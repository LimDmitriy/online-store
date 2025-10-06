from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите название продукта"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите описание продукта"}
        )
        self.fields["image"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Загрузите изображение продукта"}
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберете категорию продукта"}
        )
        self.fields["price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите цену продукта"}
        )

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError(f"Введите корректную цену")
        return price

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        black_list = [
            "казино",
            "биржа",
            "обман",
            "криптовалюта",
            "дешево",
            "полиция",
            "крипта",
            "бесплатно",
            "радар",
        ]
        name_lower = name.lower()
        description_lower = description.lower()

        for word in black_list:
            if word in name_lower or word in description_lower:
                self.add_error("name", f"Нельзя использовать слово {word}")
                break
        return cleaned_data
