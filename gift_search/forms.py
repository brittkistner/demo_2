from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from django import forms
from gift_search.models import User


class EmailUserCreationForm(UserCreationForm):
    helper = FormHelper()
    helper.form_method="POST"
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('Register', 'Register', css_class='btn-default'))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )