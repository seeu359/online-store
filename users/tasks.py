from celery import shared_task

from users.models import User, EmailVerification


@shared_task
def send_vrf_email(user_id):
    user = User.objects.get(id=user_id)
    record = EmailVerification.objects.create(user=user)
    record.send_verification_email()
