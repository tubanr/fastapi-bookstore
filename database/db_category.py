from routers.schemas import CategoryBase, CategoryDisplay, BookDisplay
from sqlalchemy.orm.session import Session
from database.models import Category


def create_category(category: CategoryBase, db:Session):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category




# get all categories with associated books
def get_all_categories(db: Session):
    categories = db.query(Category).all()
    category_display_list = []

    for category in categories:
        category_display = CategoryDisplay(
            id=category.id,
            name=category.name,
            books=[BookDisplay.from_orm(book) for book in category.books]
        )
        category_display_list.append(category_display)

    return category_display_list





# get a single category from database based on the category_id
def get_category(category_id: int, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    return category




def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).get(category_id)
    if db_category:
        # Delete associated books
        for book in db_category.books:
            db.delete(book)
        db.delete(db_category)
        db.commit()
        return True
    return False







