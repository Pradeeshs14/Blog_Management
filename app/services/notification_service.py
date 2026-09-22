from datetime import datetime

from app.services.email_service import send_email


def send_post_notification(
    recipient: str,
    recipient_name: str,
    post_title: str,
    actor_name: str,
    activity: str,
):
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    subject = f"New Activity on Your Post: {post_title}"

    body = (
        f"Hello {recipient_name},\n\n"
        f"Post: {post_title}\n"
        f"User: {actor_name}\n"
        f"Activity: {activity}\n"
        f"Time: {timestamp}\n\n"
        f"Thank you,\n"
        f"Blog Management API"
    )

    send_email(
        recipient=recipient,
        subject=subject,
        body=body,
    )