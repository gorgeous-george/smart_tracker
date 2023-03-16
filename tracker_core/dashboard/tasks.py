from celery import shared_task
from dashboard.models import CoreObject
from django.core.mail import send_mail

@shared_task
def digest():
    coreobjects = CoreObject.objects.all()
    user_ids = set(coreobjects.values_list('responsible', flat=True).distinct())
    for user_id in user_ids:
        user_objects = coreobjects.filter(responsible=user_id)
        user_red_count = len(user_objects.filter(status='Red'))
        user_name = user_objects.first().responsible.username  # get username of first object for this user
        user_email = user_objects.first().responsible.email  # get email of first object for this user
        subject = f'Hello {user_name}! Here is your fresh digest.'
        message = f'You have {user_red_count} red objects.'
        from_email = 'admin@smart_tracker.com'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)
        print(f'digest email was sent to user {user_name}, {user_email}')


@shared_task
def daily_review_reminder():
    coreobjects = CoreObject.objects.all()
    user_ids = set(coreobjects.values_list('responsible', flat=True).distinct())
    for user_id in user_ids:
        user_objects = coreobjects.filter(responsible=user_id)
        need_review = [coreobject.name for coreobject in user_objects.filter(timeframe='Day')]
        user_name = user_objects.first().responsible.username  # get username of first object for this user
        user_email = user_objects.first().responsible.email  # get email of first object for this user
        subject = f'Hello {user_name}! It is time to review your objects.'
        message = f'Daily check: {need_review}'
        from_email = 'admin@smart_tracker.com'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)
        print(f'Daily review reminder was sent to user {user_name}, {user_email}')


@shared_task()
def test():
    print('Hello from Celery!')
