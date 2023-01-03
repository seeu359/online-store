import uuid
from datetime import timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):

    image = models.ImageField(upload_to='users_image', blank=True, null=True)
    is_verified_email = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class EmailVerification(models.Model):

    code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=now() + timedelta(hours=48))

    def __str__(self):
        return f'EmailVRFCT for {self.user.email}'

    def send_verification_email(self):

        verify_link_path = reverse('users:email_ver', args=(
            self.user.email, self.code,
        ))

        link = urljoin(settings.DOMAIN_NAME, verify_link_path)
        subject = f'Подтверждение почты для {self.user.username}'

        send_mail(
            subject=subject,
            message=f'Verify your email by the following link: {link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
        )

    def is_expired(self):
        return now() >= self.expiration
