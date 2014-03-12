from django import forms
from shop.views.checkout import CheckoutSelectionView
from shop.models import AddressModel
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView
from django.views.generic import FormView
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

class HomePageView(TemplateView):
    template_name = "stables_shop/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all().order_by('status', '-id')
        context['products'] = Product.objects.all().order_by('active')
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

    def clean(self):
        data = super(ShipForm, self).clean()
        if 'target' not in data:
            try:
                data['target'] = UserProfile.objects.find(
                    data['order'].shipping_address_text)
                del self.errors['target']
            except UserProfile.DoesNotExist:
                self.errors['target'] = ErrorList(
                        [_('User "%s" not found') % data['order'].shipping_address_text])
        else:
            data['order'].shipping_address_text = data['target'].__unicode__()
            data['order'].save()
        return data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = DefaultHelper(self)
        self.helper.form_tag = True
        self.helper.disable_csrf = False
        self.helper.layout.append(
                    Submit('save', _('Save')),
                )

class EditProduct(UpdateView):
    model = Product
    template_name = "stables/generic_form.html"
    form_class = ProductForm

class PayForm(DefaultForm):
    order = forms.ModelChoiceField(queryset=Order.objects.all())
    amount = forms.DecimalField(localize=True)
    transaction_id = forms.CharField()
    payment_method = forms.CharField()

class PayView(FormView):
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

class ShipView(FormView):
    template_name = 'stables_shop/generic_form.html'
    success_url = '/s' #TODO: Bad!
    form_class = ShipForm

    def form_valid(self, form):
        from shop.shipping import api
        DigitalShipping(api.ShippingAPI()).ship(form.cleaned_data['order'])
        return super(ShipView, self).form_valid(form)
