from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from routers.schemas import UserRole


# Define the User model
class User(Base):  
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String)
    role = Column(Enum(UserRole), default="user")

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")

     

# Define the Book model
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    image_url =  Column(String)
    price = Column(Float)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship("Author", back_populates="books")

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="books")

    reviews = relationship("Review", back_populates="book")
    order_lines = relationship("OrderLine", back_populates="book")


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey("users.id"))
    

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
 


# Define the author model
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String)

    books = relationship("Book", back_populates="author")


# Define the category model
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Book", back_populates="category")



# Define the order model
class Order(Base): 
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_status = Column(Enum('pending', 'processing','shipped', 'delivered', name = 'order_status_enum'), default='pending')

    user = relationship("User", back_populates="orders")
    order_lines = relationship("OrderLine", back_populates="order")

#when the order created send email, order createing connected to post order operation
#adress and postcode  
#Define the OrderLine model 
class OrderLine(Base):
    __tablename__ = "order_lines"     

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="order_lines")
    book = relationship("Book", back_populates="order_lines")               



