from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_order
from routers.schemas import OrderSchema, OrderCreateSchema, UserAuth, UserOrder,OrderStatusEnum
from database.models import Order, OrderLine,User
from auth.oauth2 import get_current_user,get_current_user_role
from typing import List


router = APIRouter(
    prefix="/orders",
    tags=['order']
)

@router.post("", response_model=OrderSchema)
def create_order(

    order_request: OrderCreateSchema,

    current_user: UserAuth = Depends(get_current_user), 
    db: Session = Depends(get_db),
    current_user_role: str = Depends(get_current_user_role)):

    if current_user_role !=  "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Insufficient privileges")
        
    return db_order.create_order(db, order_request, current_user.id)

 


@router.get('', response_model=List[OrderSchema])
def get_user_orders( 
    user_id: int = None, db:Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_order.get_user_orders(user_id, db)

#check this one
@router.get('/{order_id}')
def get_order(
    order_id:int,
    db:Session =Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)):
    return db_order.get_order_by_id(order_id,db)




@router.put('/{order_id}', response_model=OrderSchema)
def update_order_status(
    order_id: int,
    status_update: OrderStatusEnum,
    db: Session = Depends(get_db),
    current_user_role: str =Depends(get_current_user_role)):
    
    if current_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Insufficient privileges")
    return db_order.update_order_status(db, order_id, status_update)


























#@router.delete("/{review_id}")
#def delete_order_by_id(order_id: int, db: Session = Depends(get_db),current_user: UserAuth = Depends(get_current_user)):
#    success = db_order.delete_order_by_id(db, order_id, current_user)
#    if not success:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "order not found" )
#    return {"detail": "Order deleted"}