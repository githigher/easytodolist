# backend/app/routers/todos.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app import crud, models, security
# --- MODIFIED IMPORTS ---
from app.schemas import todo as todo_schemas
# --- END MODIFIED IMPORTS ---
from app.db.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["todos & tags"],
    dependencies=[Depends(security.get_current_user)]
)

# Todos Endpoints
@router.post("/todos/", response_model=todo_schemas.Todo, status_code=status.HTTP_201_CREATED) # <-- MODIFIED HERE
def create_todo_for_user(
    todo: todo_schemas.TodoCreate, # <-- MODIFIED HERE
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)

@router.get("/todos/", response_model=List[todo_schemas.Todo]) # <-- MODIFIED HERE
def read_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    todos = crud.get_todos_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return todos

@router.put("/todos/{todo_id}", response_model=todo_schemas.Todo) # <-- MODIFIED HERE
def update_todo(
    todo_id: int,
    todo_update: todo_schemas.TodoUpdate, # <-- MODIFIED HERE
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    return crud.update_todo(db=db, db_todo=db_todo, todo_update=todo_update, user_id=current_user.id)

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")
    crud.delete_todo(db=db, db_todo=db_todo)
    return

# Tags Endpoints
@router.post("/tags/", response_model=todo_schemas.Tag, status_code=status.HTTP_201_CREATED) # <-- MODIFIED HERE
def create_tag_for_user(
    tag: todo_schemas.TagCreate, # <-- MODIFIED HERE
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    return crud.create_user_tag(db=db, tag=tag, user_id=current_user.id)

@router.get("/tags/", response_model=List[todo_schemas.Tag]) # <-- MODIFIED HERE
def read_tags(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    tags = crud.get_tags_by_user(db, user_id=current_user.id)
    return tags


@router.put("/tags/{tag_id}", response_model=todo_schemas.Tag)
def update_tag(
        tag_id: int,
        tag_update: todo_schemas.TagBase,  # TagBase 只有 name 字段，正好适用
        db: Session = Depends(get_db),
        current_user: models.User = Depends(security.get_current_user)
):
    db_tag = crud.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    # 关键安全检查：确保标签属于当前用户
    if db_tag.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this tag")

    return crud.update_tag(db=db, db_tag=db_tag, tag_update=tag_update)


@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
        tag_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(security.get_current_user)
):
    db_tag = crud.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    # 关键安全检查：确保标签属于当前用户
    if db_tag.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this tag")

    crud.delete_tag(db=db, db_tag=db_tag)
    return Response(status_code=status.HTTP_204_NO_CONTENT)