from django import forms
from shop.views.checkout import CheckoutSelectionView
from shop.models import AddressModel
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView
from shop.models import Order
from shop.models import Product
from stables_shop.backends import DigitalShipping
from stables.models import UserProfile
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import ButtonHolder
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned

class DefaultHelper(FormHelper):
    label_class = "col-xs-2"
    field_class = "col-xs-10"
    form_tag = False
    disable_csrf = True

def ret_name(self):
    return self.name

funcType = type(AddressModel.as_text)

class NoShippingForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ['name', ]

    def save(self):
        obj = super(forms.ModelForm, self).save()
        obj.as_text = funcType(ret_name, obj, AddressModel)
        return obj

class FinnishPaymentForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ['name', 'address', 'zip_code', 'city' ]

    def save(self):
        obj = super(forms.ModelForm, self).save()
        return obj

class NoShippingAddressCheckoutSelectionView(CheckoutSelectionView):
    def get_shipping_form_class(self):
        return NoShippingForm

    def get_billing_form_class(self):
        return FinnishPaymentForm

    def get_shipping_address_form(self):
        form = super(NoShippingAddressCheckoutSelectionView, self).get_shipping_address_form()
        form.helper = DefaultHelper()
        return form

    def get_billing_address_form(self):
        form = super(NoShippingAddressCheckoutSelectionView, self).get_billing_address_form()
        form.helper = DefaultHelper()
        return form

    def get_extra_info_form(self):
        form = super(NoShippingAddressCheckoutSelectionView, self).get_extra_info_form()
        form.helper = DefaultHelper()
        return form

    def get_billing_and_shipping_selection_form(self):
        form = super(NoShippingAddressCheckoutSelectionView, self).get_billing_and_shipping_selection_form()
        form.fields['shipping_method'].widget.attrs['class'] = "hidden"
        form.fields['shipping_method'].label = ""
        form.helper = DefaultHelper()
        return form

class ShopRedirectView(RedirectView):
    def get_redirect_url(self):
        return reverse('product_list')

_products = None
def products():
    global _products
    if _products == None:
        _products = {}
        for ct in ContentType.objects.filter(app_label='stables_shop'):
            if issubclass(ct.model_class(), Product):
                _products[ct.model_class()] = ct
    return _products

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

class ShopEditorMixin(object):
    @method_decorator(permission_required('shop.change_product'))
    def dispatch(self, request, *args, **kwargs):
        return super(ShopEditorMixin, self).dispatch(request, *args, **kwargs)


class HomePageView(ShopEditorMixin, TemplateView):
    template_name = "stables_shop/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all().order_by('status', '-id')
        context['products'] = Product.objects.all().order_by('active')
        context['newproducts'] = products()
        return context

class DefaultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.helper = DefaultHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_tag = True
        self.helper.disable_csrf = False

class ShipForm(DefaultForm):
    order = forms.ModelChoiceField(queryset=Order.objects.all())
    target = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    target_name = forms.CharField(required=False)

    def clean(self):
        data = super(ShipForm, self).clean()
        if 'target' not in data:
            if 'target_name' in data:
                data['order'].shipping_address_text = data['target_name']
                data['order'].save()
            try:
                data['target'] = UserProfile.objects.find(
                    data['order'].shipping_address_text)
                del self.errors['target']
            except UserProfile.DoesNotExist:
                self.errors['target'] = ErrorList(
                        [_('User "%s" not found') % data['order'].shipping_address_text])
            except MultipleObjectsReturned:
                self.errors['target'] = ErrorList(
                        [_('User "%s" is too ambiguous') % data['order'].shipping_address_text])
        else:
            data['order'].shipping_address_text = data['target'].__unicode__()
            data['order'].save()
        return data

def prodform(prodmodel):
    class ProductForm(forms.ModelForm):
        class Meta:
            model = prodmodel

        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_tag = True
            self.helper.disable_csrf = False
            self.helper.layout.append(
                      ButtonHolder(
                        Submit('save', _('Save')),
                        )
                    )
    return ProductForm


class EditProduct(ShopEditorMixin, UpdateView):
    model = Product
    template_name = "stables_shop/generic_form.html"
    def get_form_class(self):
        return prodform(self.object.__class__)

class CreateProduct(ShopEditorMixin, CreateView):
    model = Product
    template_name = "stables_shop/generic_form.html"

    def get_form_class(self):
        ct = ContentType.objects.get(pk=self.kwargs['content_type_id'])
        return prodform(ct.model_class())

class FinishedOrderList(ShopEditorMixin, ListView):
    model = Order
    template_name = "stables_shop/order_list.html"
    context_object_name = 'order_list'

    queryset = Order.objects.all().order_by('-id')

class PayForm(DefaultForm):
    order = forms.ModelChoiceField(queryset=Order.objects.all())
    amount = forms.DecimalField(localize=True)
    transaction_id = forms.CharField()
    payment_method = forms.CharField()

class PayView(ShopEditorMixin, FormView):
    template_name = 'stables_shop/generic_form.html'
    success_url = '/s' #TODO: Bad!
    form_class = PayForm

    def form_valid(self, form):
        from shop.payment import api
        api.PaymentAPI().confirm_payment(
                form.cleaned_data['order'],
                form.cleaned_data['amount'],
                form.cleaned_data['transaction_id'],
                form.cleaned_data['payment_method'],
                )
        return super(PayView, self).form_valid(form)

class ShipView(ShopEditorMixin, FormView):
    template_name = 'stables_shop/generic_form.html'
    success_url = '/s' #TODO: Bad!
    form_class = ShipForm

    def form_valid(self, form):
        from shop.shipping import api
        DigitalShipping(api.ShippingAPI()).ship(form.cleaned_data['order'])
        return super(ShipView, self).form_valid(form)
