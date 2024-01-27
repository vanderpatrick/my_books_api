import sqlalchemy as s
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = "author"

    id: int = s.Column(s.Integer, primary_key=True, index=True)
    name: str = s.Column(s.String)
    country_origin: str = s.Column(s.String)
    total_books: int = s.Column(s.Integer)
    created: str = s.Column(s.String)
    updated: str = s.Column(s.String, nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "book"

    id = s.Column(s.Integer, primary_key=True, index=True)
    book_title = s.Column(s.String)
    book_author_id = s.Column(s.Integer, s.ForeignKey("author.id"))
    book_index_by_author = s.Column(s.Integer)
    created = s.Column(s.String)
    updated = s.Column(s.String, nullable=True)

    author = relationship("Author", back_populates="books")
