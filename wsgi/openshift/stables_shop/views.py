from django import forms
from shop.views.checkout import CheckoutSelectionView
from shop.models import AddressModel

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
