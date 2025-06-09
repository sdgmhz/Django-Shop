from django import forms

from order.models import UserAddressModel

class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddressModel
        fields = [
            "address",
            "state",
            "city",
            "zip_code",
        ]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].widget.attrs["class"] = "form-control"
        self.fields["state"].widget.attrs["class"] = "form-control"
        self.fields["city"].widget.attrs["class"] = "form-control"
        self.fields["zip_code"].widget.attrs["class"] = "form-control"
        self.fields["address"].widget.attrs[
            "placeholder"
        ] = "آدرس را وارد نمایید"
        self.fields["state"].widget.attrs[
            "placeholder"
        ] = "استان را وارد نمایید"
        self.fields["city"].widget.attrs[
            "placeholder"
        ] = "شهر را وارد نمایید"
        self.fields["zip_code"].widget.attrs[
            "placeholder"
        ] = "کدپستی را وارد نمایید"