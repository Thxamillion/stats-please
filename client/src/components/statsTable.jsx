import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Box } from '@mui/material';
import { ThumbUp, ThumbDown } from '@mui/icons-material';

const DataTable = ({ data }) => {
  const columns = Object.keys(data[0]);

  return (
    <TableContainer component={Paper} sx={{ maxWidth: 800, marginTop: '50px', marginX: 'auto' }}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            {columns.map(column => (
              <TableCell key={column}>
                {column}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index}>
              {columns.map(column => (
                <TableCell key={column}>
                  {row[column]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

const SummaryTable = ({ data }) => {
  const columns = Object.keys(data[0]);

   const averages = columns.reduce((acc, column) => {
    const values = data.map(row => row[column]);
    const sum = values.reduce((total, value) => total + value, 0);
    const average = (sum / values.length).toFixed(3);
    return { ...acc, [column]: average };
  }, {});

  // Calculate totals
  const totals = columns.reduce((acc, column) => {
    const values = data.map(row => row[column]);
    const total = values.reduce((total, value) => total + value, 0);
    return { ...acc, [column]: total };
  }, {});

  return (
    <TableContainer component={Paper} sx={{ maxWidth: 800, marginTop: '50px', marginX: 'auto' }}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Column</TableCell>
            <TableCell>Average</TableCell>
            <TableCell>Total</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {columns.map(column => (
            <TableRow key={column}>
              <TableCell>{column}</TableCell>
              <TableCell>{averages[column]}</TableCell>
              <TableCell>{totals[column]}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

const StatsTable = ({ data, sqlQuery }) => {
  const [feedback, setFeedback] = useState('');

  if (data.length === 0) {
    return (
      <Box>
        <p>No results found</p>
        <p>Sorry, I didn't understand your question. Here is my SQL query:</p>
        <pre>{sqlQuery}</pre>
        <Box display="flex" justifyContent="center" alignItems="center" marginTop={2}>
          <Button variant="contained" color="primary" onClick={() => setFeedback('Looks correct')}>
            <ThumbUp />
          </Button>
          <Button variant="contained" color="error" onClick={() => setFeedback('Error in SQL query')}>
            <ThumbDown />
          </Button>
        </Box>
        <p>{feedback}</p>
      </Box>
    );
  }

  return (
    <Box>
      <DataTable data={data} />
      <SummaryTable data={data} />
      </Box>
  );
};

export default StatsTable;
