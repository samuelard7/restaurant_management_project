from django from forms
from utils.validation_utils import validate_email_address

class UserProfileForm(forms.Form):
    email = forms.EmailField(label="Email Address")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_valid, message = validate_email_address(email)
        if not is_valid:
            raise forms.ValidationError(message)
        return email