import schemas, database, models
from oauth2 import get_current_user
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/blog",
  tags=['Blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
  blogs = db.query(models.Blog).all()
  return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
  new_blog = models.Blog(time=request.time, body=request.body, user_id=1)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} isn't found!")
  blog.delete(synchronize_session=False)
  db.commit()
  return 'blog has been deleted!'


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} isn't found!")
  blog.update(request.dict())
  db.commit()
  return 'blog updated!'


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(database.get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} isn't available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"Blog with the id {id} isn't available"}
  return blog