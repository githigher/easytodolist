# backend/app/crud.py

from sqlalchemy.orm import Session
from app import models, security
# --- MODIFIED IMPORTS ---
from app.schemas import user as user_schemas
from app.schemas import todo as todo_schemas


# --- END MODIFIED IMPORTS ---

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: user_schemas.UserCreate):  # <-- MODIFIED HERE
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Tag CRUD
def get_tags_by_user(db: Session, user_id: int):
    return db.query(models.Tag).filter(models.Tag.owner_id == user_id).all()


def create_user_tag(db: Session, tag: todo_schemas.TagCreate, user_id: int):  # <-- MODIFIED HERE
    db_tag = models.Tag(**tag.model_dump(), owner_id=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


# Todo CRUD
def get_todos_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).offset(skip).limit(limit).all()


def create_user_todo(db: Session, todo: todo_schemas.TodoCreate, user_id: int):  # <-- MODIFIED HERE
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        owner_id=user_id
    )
    # 关联标签
    if todo.tags:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(todo.tags), models.Tag.owner_id == user_id).all()
        db_todo.tags.extend(tags)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def update_todo(db: Session, db_todo: models.Todo, todo_update: todo_schemas.TodoUpdate,
                user_id: int):  # <-- MODIFIED HERE
    update_data = todo_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "tags":
            if value is not None:
                tags = db.query(models.Tag).filter(models.Tag.id.in_(value), models.Tag.owner_id == user_id).all()
                db_todo.tags = tags
        else:
            setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, db_todo: models.Todo):
    db.delete(db_todo)
    db.commit()


def update_tag(db: Session, db_tag: models.Tag, tag_update: todo_schemas.TagBase):
    """Updates a tag's name."""
    db_tag.name = tag_update.name
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, db_tag: models.Tag):
    """Deletes a tag."""
    # SQLAlchemy 会自动处理多对多关系表中的关联记录
    db.delete(db_tag)
    db.commit()