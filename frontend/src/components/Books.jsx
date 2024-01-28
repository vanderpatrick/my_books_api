// BookList.js
import React, { useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import axios from 'axios';

const BookList = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get('http://0.0.0.0:8080/book/all');
        setBooks(response.data);
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    };

    fetchBooks();
  }, []);

  return (
    <div style={{ marginTop: '80px', padding: '16px', display: 'flex', flexWrap: 'wrap' }}>
      {books.map((book) => (
        <Card
          key={book.id}
          style={{
            backgroundColor: 'grey',
            marginBottom: '16px',
            marginRight: '16px',
            marginLeft: '16px', // Adjust the left margin to create space
            width: '300px',
            height: '300px',
          }}
        >
          <CardContent>
            <Typography variant="h6" color="textPrimary">
              {book.book_title}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {book.author}
            </Typography>
            {/* Add other book details as needed */}
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default BookList;
