import os

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserRegisterForm
from .models import User
from django.core.mail import send_mail


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)

        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать на нас сервис"
        message = "Спасибо что зарегистрировались на нашем сайте"
        from_email = os.getenv("EMAIL_HOST")
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)
