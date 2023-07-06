from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from .schemas import CategoryBase, CategoryDisplay,BookDisplay
from database import db_category
from database.models import Category
from typing import List

router = APIRouter(
    prefix='/categories',
    tags=['category']
)

@router.post("", response_model=CategoryDisplay)
def create_category(category: CategoryBase, db: Session = Depends(get_db)):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("", response_model=List[CategoryDisplay])
def get_all_categories(db: Session = Depends(get_db)):
    categories = db_category.get_all_categories(db)
    return categories


# Define route to retrieve a single category by its ID
@router.get("/{category_id}", response_model=CategoryDisplay) 
def Specific_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        # Raise HTTPException with 404 status code
        raise HTTPException(status_code=404, detail="Category not found")
    category_display = CategoryDisplay(
        id=category.id,
        name=category.name,
        books=[BookDisplay.from_orm(book) for book in category.books]

    )
    return category_display





@router.delete('/{category_id}')
def delete_category(category_id: int, db: Session = Depends(get_db)):
    success = db_category.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
    return {'message': 'category deleted successfully'}


