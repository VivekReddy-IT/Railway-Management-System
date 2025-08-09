import React, { useContext } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
} from '@mui/material';
import {
  DirectionsRailway as TrainIcon,
  AccountCircle,
  Menu as MenuIcon,
} from '@mui/icons-material';
import { AuthContext } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static" elevation={0} sx={{ backgroundColor: 'white' }}>
        <Toolbar>
        <TrainIcon sx={{ color: 'primary.main', mr: 1 }} />
          <Typography
            variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'primary.main',
            fontWeight: 'bold',
          }}
        >
          Rail Transit
        </Typography>

        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 2 }}>
          <Button
            component={RouterLink}
            to="/search"
            color="primary"
            variant="outlined"
          >
            Search Trains
          </Button>
          {user ? (
            <>
              <Button
                component={RouterLink}
                to="/profile"
                color="primary"
                variant="outlined"
              >
                My Bookings
              </Button>
              <IconButton
                onClick={handleMenu}
                color="primary"
                sx={{ ml: 1 }}
              >
                <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                  {user.username?.[0]?.toUpperCase()}
                </Avatar>
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem
                  component={RouterLink}
                  to="/profile"
                  onClick={handleClose}
                >
                  Profile
                </MenuItem>
                <MenuItem onClick={() => {
                  handleClose();
                  logout();
                }}>
                  Logout
                </MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button
                component={RouterLink}
                to="/login"
                color="primary"
                variant="outlined"
              >
              Login
            </Button>
              <Button
                component={RouterLink}
                to="/register"
                color="primary"
                variant="contained"
              >
                Register
              </Button>
            </>
          )}
        </Box>

        <IconButton
          sx={{ display: { xs: 'flex', md: 'none' } }}
          color="primary"
          onClick={handleMenu}
        >
          <MenuIcon />
        </IconButton>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleClose}
          sx={{ display: { xs: 'block', md: 'none' } }}
        >
          <MenuItem component={RouterLink} to="/search" onClick={handleClose}>
            Search Trains
          </MenuItem>
          {user ? (
            <>
              <MenuItem component={RouterLink} to="/profile" onClick={handleClose}>
                My Bookings
              </MenuItem>
              <MenuItem onClick={() => {
                handleClose();
                logout();
              }}>
                Logout
              </MenuItem>
            </>
          ) : (
            <>
              <MenuItem component={RouterLink} to="/login" onClick={handleClose}>
                Login
              </MenuItem>
              <MenuItem component={RouterLink} to="/register" onClick={handleClose}>
                Register
              </MenuItem>
            </>
          )}
        </Menu>
        </Toolbar>
      </AppBar>
  );
};

export default Navbar; 