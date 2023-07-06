from fastapi import APIRouter,UploadFile,File
from typing import List
import string
import random
import shutil


router = APIRouter(prefix="/images", tags=["images"])


#To make image folder accessible statically
@router.post('/')
def upload_image(image: UploadFile = File(...)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}