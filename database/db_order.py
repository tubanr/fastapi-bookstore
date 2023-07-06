from sqlalchemy.orm import Session
from routers.schemas import OrderCreateSchema,OrderSchema,UserAuth, OrderStatusEnum
from database.models import Order, OrderLine,User
from fastapi import HTTPException, status
from  auth.oauth2 import get_current_user_role
from email_utils import send_email


def create_order(db: Session, order_request: OrderCreateSchema, user_id:int):
    order = Order(user_id=user_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    # create order lines
    order_lines =[]
    for order_line_request in order_request.order_lines:
        book_id = order_line_request.book_id
        quantity = order_line_request.quantity
        order_line =OrderLine(order_id=order.id, book_id=book_id, quantity=quantity)
        db.add(order_line)
        db.commit()
        db.refresh(order_line)
        order_lines.append(order_line)

    order.order_lines = order_lines
    db.add(order)
    db.commit()

    subject = "New order"
    content = f"You received new order with ID: {order_line.order_id}. Click the link to check the order details"
    recipient_email ="admin@gmail.com"
    send_email(recipient_email, subject,content)

    db.refresh(order)

    return order




# get orders of an spesific user by user ID
def get_user_orders(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.orders



def get_order_by_id(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id==order_id).first()
     
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
        


def update_order_status(db:Session, order_id:int, order_status: OrderStatusEnum):
    order =db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Order not found")
    order.order_status= order_status
    db.commit()
    db.refresh(order)
    return order










































#def delete_order_by_id(db: Session, order_id: int, user_id:int, current_user: UserAuth):
#    db_order = db.query(Order).get(order_id)
#    if db_order is not None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
#        db.delete(db_order)
#        db.commit()
#        return True
#    return False