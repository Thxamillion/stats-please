import React from 'react';
import { AppBar, Toolbar, Typography } from '@material-ui/core';

const Navbar = () => (
  <AppBar position="static" style={{ margin: 0 }}>
    <Toolbar variant="dense">
      <Typography variant="h6" color="inherit" component="div">
        Stats Please
      </Typography>
    </Toolbar>
  </AppBar>
);

export default Navbar;
