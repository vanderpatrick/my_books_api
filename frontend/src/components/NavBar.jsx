// Navbar.js
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

const Navbar = () => {
  return (
    <AppBar position="fixed" style={{ backgroundColor: 'black' }}>
      <Toolbar>
        <Typography variant="h6" color="inherit">
          My Books
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
