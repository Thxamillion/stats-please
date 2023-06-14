import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography } from '@material-ui/core';

const Navbar = () => {
    const navigate = useNavigate();


    return (
    <AppBar position="static" style={{ margin: 0 }}>
        <Toolbar variant="dense">
        <Typography variant="h6" color="#3f50b5" component="div" fontWeight="bold"
        fontSize="clamp(1rem, 2rem, 2.25rem)"
        onClick={() => navigate("/ask")}
        sx={{
          "&:hover": {
            color: "black",
            cursor: "pointer"
          },
        }}
      >
            Stats Please
        </Typography>
        </Toolbar>
    </AppBar>
);
}
export default Navbar;
