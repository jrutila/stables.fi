from django import forms
from shop.views.checkout import CheckoutSelectionView
from shop.models import AddressModel
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from shop.models import Order
from stables_shop.backends import DigitalShipping
from stables.models import UserProfile
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class DefaultHelper(FormHelper):
    def __init__(self):
        super(DefaultHelper, self).__init__()
        self.add_input(Submit('submit', 'Submit'))

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

class NoShippingAddressCheckoutSelectionView(CheckoutSelectionView):
    def get_shipping_form_class(self):
        return NoShippingForm

class HomePageView(TemplateView):
    template_name = "stables_shop/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        #order = context['orders'][0]
        #import pdb; pdb.set_trace()
        return context

class DefaultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.helper = DefaultHelper()

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
