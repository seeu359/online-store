from celery import shared_task

from users.models import EmailVerification, User


@shared_task
def send_vrf_email(user_id):
    user = User.objects.get(id=user_id)
    record = EmailVerification.objects.create(user=user)
    record.send_verification_email()
