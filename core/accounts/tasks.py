from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_reset_email_task(
    subject_template_name,
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name=None,
):
    """Asynchronously sends password reset email using Celery"""
    subject = render_to_string(subject_template_name, context).replace("\n", "")
    body = render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name:
        html_body = render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_body, "text/html")

    email_message.send()
