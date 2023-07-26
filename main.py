from fastapi import FastAPI
from routers import user, book, author, category, review, order,image
from database import models
from database.database import engine
from auth import authentication
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
app.include_router(user.router)
app.include_router(book.router)
app.include_router(author.router)
app.include_router(category.router)
app.include_router(review.router)
app.include_router(order.router)
app.include_router(authentication.router)
app.include_router(image.router)

@app.get("/")
def index():
    return 'Hello world'

origins =[
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(engine)

app.mount("/images", StaticFiles(directory='images'), name='images')