import React, { useState } from 'react';
import { Paper, Typography, Button, Box } from '@mui/material';
import { ThumbUp, ThumbDown } from '@mui/icons-material';

const Billboard = ({ query,sqlQuery }) => {
  const [feedback, setFeedback] = useState('');

  const handleThumbsUp = () => {
    setFeedback('Looks correct');
    // if user puts thumbs up, query looks correct but no results found. Will log and double check
  };

  const handleThumbsDown = () => {
    setFeedback('Error in SQL query');
    // will log soon to see what went wrong and imporve
  };

  return (
    <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6">Your Query:</Typography>
      <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>{query}</Typography>
      <Typography variant="h6">SQL Query:</Typography>
      <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>{sqlQuery}</Typography>

      <Box display="flex" justifyContent="center" alignItems="center" marginTop={2}>
        <Button variant="contained" color="primary" onClick={handleThumbsUp}>
          <ThumbUp />
        </Button>
        <Button variant="contained" color="error" onClick={handleThumbsDown}>
          <ThumbDown />
        </Button>
      </Box>
      <Typography variant="body2">{feedback}</Typography>
    </Paper>
  );
};

export default Billboard;
