from typing import Annotated, Union, List
from starlette import status
from pydantic import BaseModel
from database import engine, SessionLocal as DB
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, Request, Form
import datetime as dt
import models as m


router = APIRouter(prefix="/book", tags=["Book"])


def get_db():
    try:
        DB()
        yield DB()
    finally:
        DB().close()


db_dependency = Annotated[Session, Depends(get_db)]


# Endregion
# Start Region Book
# create Pydentic request model
class BookRequest(BaseModel):
    book_title: str
    book_author_id: int
    book_index_by_author: int


class BookResponse(BaseModel):
    id: int
    book_author_id: int
    book_index_by_author: int
    created: str
    book_title: str
    updated: str


# Get all author from database
@router.get(
    "/all",
    status_code=status.HTTP_302_FOUND,
    response_model=List[BookResponse],
)
async def get_all_books(db: Session = Depends(get_db)):
    book = db.query(m.Book).filter().all()

    if not book:
        raise HTTPException(status_code=404, detail="There are no books at the moment")

    # Convert the database results to the desired response format using the Pydantic model
    book_response = [
        BookResponse(
            id=record.id,
            book_author_id=record.book_author_id,
            book_index_by_author=record.book_index_by_author,
            book_title=record.book_title,
            created=record.created,
            updated=record.updated if record.updated else "",
        )
        for record in book
    ]

    return book_response


# create instance of author
@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_book(db: db_dependency, book_request: Union[BookRequest or bool]):
    existing_author = (
        db.query(m.Author).filter(m.Author.id == book_request.book_author_id).first()
    )

    if existing_author:
        new_book = m.Book(
            book_title=book_request.book_title,
            book_author_id=book_request.book_author_id,
            book_index_by_author=book_request.book_index_by_author,
            created=dt.datetime.today(),
        )
        db.add(new_book)
        db.commit()

        return {"Message": "Book created with success."}
    else:
        return {"Message": "Author not found."}


# create update instance of author
@router.put(
    "/edit/{book_id}",
    status_code=status.HTTP_200_OK,
)
async def update_book(
    db: db_dependency, book_request: BookRequest, book_id: Union[int or bool]
):
    book = db.query(m.Book).filter(m.Author.id == book_id).first()
    if book:
        book.book_author_id = book_id
        book.book_index_by_author = book_request.book_index_by_author
        book.book_title = book_request.book_title
        book.updated = dt.datetime.today()
        db.commit()
        return {"Message": "Author updated success."}
    else:
        raise HTTPException(status_code=404, detail="Author Not found")


# delete instance of author
@router.delete(
    "/delete/{book_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_book(db: db_dependency, book_id: Union[int or bool]):
    record = db.query(m.Book).filter(m.Book.id == book_id).first()
    if record:
        db.delete(record)
        db.commit()
        return {"message": "Book Deleted with success"}
    else:
        raise HTTPException(status_code=404, detail="Author Not found")
