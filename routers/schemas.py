from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class UserRole(str,Enum):
    admin="admin"
    user="user"

class UserBase(BaseModel):
    username: str
    email: Optional[str] 
    password: str
    role:  Optional[UserRole ] = 'user' # default value as a user


class UserDisplay(BaseModel):
    username: str
    email: Optional[str] 
    role: Optional[str] 
    
    
    class Config():
        orm_mode =  True


# require this structure-request
class BookBase(BaseModel):
    title: str
    description: str
    price: float
    image_url: str
    author_id: int
    category_id: int


# define the request structure for creating a category
class CategoryBase(BaseModel):
    name: str

    class Config():
        orm_mode = True


class AuthorDisplay(BaseModel):
    id: int
    name: str

    class Config():
        orm_mode = True


# Author for BookDisplay
class Author(BaseModel):
    name: str

    class Config():
        orm_mode = True



#Schema for displaying reviews details
class ReviewDisplay(BaseModel):
    id: int
    text: str
    book_id: int
    user:  UserDisplay
    
    
    class Config():
        orm_mode = True



# Display this structure-response for books
class BookDisplay(BaseModel):
    id: int
    title: str
    description: str
    price: float
    image_url: str
    reviews: List[ReviewDisplay]
    author: Optional[Author]

    class Config():
        orm_mode = True



# Request schema for creating an author
class AuthorBase(BaseModel):
    name: str



# Schema to display books with a category
class CategoryDisplay(BaseModel):
    id: int
    name: str
    books: List[BookDisplay]

    class Config():
        orm_mode = True



class UserAuth(BaseModel):
    id: int
    username: str
    email: Optional[str]
    role: str

    class Config():
        orm_mode = True



# Schema for creating review
class ReviewBase(BaseModel):
    text: str
    book_id: int



#Schema for order line details
class OrderLineSchema(BaseModel):
    book_id: int
    quantity: int

    class Config():
        orm_mode=True


#Schema for creating a new order
class OrderCreateSchema(BaseModel):
    order_lines: List[OrderLineSchema]

    class Config():
        orm_mode=True


# Schema for updating order status
class OrderStatusEnum(str, Enum):
    pending = 'pending'
    processing = 'processing'
    shipped = 'shipped'
    delivered = 'delivered'
    


# Schema for order details
class OrderSchema(BaseModel):
    id: int
    user: UserDisplay
    order_status: OrderStatusEnum
    
    order_lines: List[OrderLineSchema]

    class Config():
        orm_mode=True




        
#schema for retrieving an users order
class UserOrder(BaseModel):
    user_id: int
    
    
    class Config():
        orm_mode=True




 




    

