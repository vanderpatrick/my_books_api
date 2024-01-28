from typing import Annotated, Union, List
from starlette import status
from pydantic import BaseModel
from database import engine, SessionLocal as DB
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, Request, Form
import datetime as dt
import models as m


router = APIRouter(prefix="/author", tags=["Author"])


def get_db():
    try:
        DB()
        yield DB()
    finally:
        DB().close()


db_dependency = Annotated[Session, Depends(get_db)]


# create Pydentic request model
class AuthorRequest(BaseModel):
    name: str
    country_origin: str
    total_books: int


class AuthorResponse(BaseModel):
    id: int
    name: str
    created: str
    updated: str
    total_books: int
    country_origin: str


# Get all author from database
@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[AuthorResponse],
)
async def get_all_author(db: Session = Depends(get_db)):
    authors = db.query(m.Author).filter().all()

    if not authors:
        raise HTTPException(
            status_code=404, detail="There are no authors at the moment"
        )

    # Convert the database results to the desired response format using the Pydantic model
    author_responses = [
        AuthorResponse(
            name=author.name,
            id=author.id,
            created=author.created,
            updated=author.updated if author.updated else "",
            total_books=author.total_books,
            country_origin=author.country_origin,
        )
        for author in authors
    ]

    return author_responses


# create instance of author
@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
async def creat_author(db: db_dependency, author_request: AuthorRequest):
    new_author = m.Author(
        name=author_request.name,
        country_origin=author_request.country_origin,
        total_books=author_request.total_books,
        created=dt.datetime.today(),
    )
    db.add(new_author),
    db.commit()
    return {
        "Message": "Author created with success.",
    }


# create update instance of author
@router.put(
    "/edit/{author_id}",
    status_code=status.HTTP_200_OK,
)
async def update_author(
    db: db_dependency, author_request: AuthorRequest, author_id: Union[int or bool]
):
    author = db.query(m.Author).filter(m.Author.id == author_id).first()
    if author:
        author.name = author_request.name
        author.country_origin = author_request.country_origin
        author.total_books = author_request.total_books
        author.updated = dt.datetime.today()
        db.commit()
        return {"Message": "Author updated success."}
    else:
        raise HTTPException(status_code=404, detail="Author Not found")


# delete instance of author
@router.delete(
    "/delete/{author_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_author(db: db_dependency, author_id: Union[int or bool]):
    record = db.query(m.Author).filter(m.Author.id == author_id).first()
    if record:
        db.delete(record)
        db.commit()
        return {"message": "author  Deleted with success"}
    else:
        raise HTTPException(status_code=404, detail="Author Not found")
