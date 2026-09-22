
from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.post import Post
from app.models.post_image import PostImage
from app.schemas.post import PostResponse, PaginatedPostResponse
from app.core.security import get_current_user
from app.models.user import User
from app.utils.subscription_limits import (
    get_active_subscription,
    check_limit,
)

import os
import uuid


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


UPLOAD_DIR = "media/posts"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=PostResponse)
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subscription, plan = get_active_subscription(
        db,
        current_user.id,
    )

    post_count = (
        db.query(Post)
        .filter(Post.author_id == current_user.id)
        .count()
    )

    check_limit(
        db,
        current_user.id,
        post_count,
        plan.max_posts,
    )

    image_path = None

    if image:
        subscription, plan = get_active_subscription(
            db,
            current_user.id,
        )

        check_limit(
            db,
            current_user.id,
            0,
            plan.max_images_per_post,
        )

        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())

        image_path = f"/media/posts/{file_name}"

    post = Post(
        title=title,
        content=content,
        author_id=current_user.id,
        image=image_path,
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    if image_path:
        post_image = PostImage(
            post_id=post.id,
            image_path=image_path,
        )

        db.add(post_image)
        db.commit()

    return post


@router.get("/", response_model=PaginatedPostResponse)
def get_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Post)

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            (Post.title.ilike(search_term))
            | (Post.content.ilike(search_term))
        )

    total = query.count()

    total_pages = (total + limit - 1) // limit

    posts = (
        query
        .order_by(Post.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "posts": posts,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


@router.get("/mine", response_model=list[PostResponse])
def get_my_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Post)
        .filter(Post.author_id == current_user.id)
        .order_by(Post.created_at.desc())
        .all()
    )


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    post.views += 1
    db.commit()

    return post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own posts",
        )

    post.title = title
    post.content = content

    if image:
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())

        post.image = f"/media/posts/{file_name}"

    db.commit()
    db.refresh(post)

    return post


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own posts",
        )

    db.delete(post)
    db.commit()

    return {
        "message": "Post deleted successfully"
    }


@router.post("/{post_id}/images")
def add_post_image(
    post_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only add images to your own posts",
        )

    subscription, plan = get_active_subscription(
        db,
        current_user.id,
    )

    image_count = (
        db.query(PostImage)
        .filter(PostImage.post_id == post_id)
        .count()
    )

    check_limit(
        db,
        current_user.id,
        image_count,
        plan.max_images_per_post,
    )

    file_extension = os.path.splitext(image.filename)[1]
    file_name = f"{uuid.uuid4()}{file_extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        file_name,
    )

    with open(file_path, "wb") as buffer:
        buffer.write(image.file.read())

    image_path = f"/media/posts/{file_name}"

    post_image = PostImage(
        post_id=post_id,
        image_path=image_path,
    )

    db.add(post_image)
    db.commit()
    db.refresh(post_image)

    return {
        "message": "Image added successfully",
        "image_id": post_image.id,
        "post_id": post_id,
        "image_path": image_path,
    }

