from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    avatar = forms.ImageField(
        label="Аватар",
        required=False,
    )
    phone_number = forms.CharField(
        max_length=15,
        label="Номер телефона",
        required=False,
    )
    country = forms.CharField(
        max_length=50,
        label="Страна",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите имя"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите фамилию"}
        )
        self.fields["avatar"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Добавьте аватар"}
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите номер телефона"}
        )
        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите страну"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторно введите пароль"}
        )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "avatar",
            "phone_number",
            "country",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError(
                "Номер телефона должен состоять только из цифр."
            )
        return phone_number
