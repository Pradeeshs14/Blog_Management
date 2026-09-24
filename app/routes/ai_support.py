from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ai_support import AISupportChat
from app.schemas.ai_support import AISupportRequest, AISupportResponse
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/api/ai-support",
    tags=["AI Support"]
)


def generate_ai_response(message: str) -> str:
    message = message.lower()

    if "create" in message and "post" in message:
        return "To create a post, go to the Posts section and use the Create Post option. Enter your content and submit the post."

    if ("edit" in message or "update" in message) and "post" in message:
        return "You can edit your own posts from the Posts section by selecting the edit option for the post."

    if "delete" in message and "post" in message:
        return "You can delete your own posts from the Posts section using the delete option."

    if "subscription" in message:
        return "You can view the available subscription plans, activate a plan, check your current subscription, and renew an active subscription from the Subscription section."

    if "billing" in message or "payment" in message:
        return "You can view your billing history from the Billing History section. It contains information about your subscription transactions."

    if "profile" in message:
        return "You can manage your account information from your profile or account section."

    if "dashboard" in message or "analytics" in message:
        return "The dashboard provides information about your posts, likes, comments, subscriptions, and other activity statistics."

    if "hello" in message or "hi" in message:
        return "Hello! 👋 I'm your AI Support Assistant. How can I help you with the blog platform?"

    return "I'm here to help with posts, comments, likes, subscriptions, billing, profile management, and dashboard features. Please ask me a question about any of these."


@router.get("/", response_model=list[AISupportResponse])
def get_ai_support_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(AISupportChat)
        .filter(AISupportChat.user_id == current_user.id)
        .order_by(AISupportChat.created_at.asc())
        .all()
    )

@router.post("/", response_model=AISupportResponse)
def ai_support(
    request: AISupportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ai_response = generate_ai_response(request.message)

    chat = AISupportChat(
        user_id=current_user.id,
        question=request.message,
        ai_response=ai_response,
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat