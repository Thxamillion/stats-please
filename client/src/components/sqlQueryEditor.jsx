import React, { useState, useEffect } from 'react';
import { TextField } from '@mui/material';

const SQLQueryEditor = ({ initialQuery }) => {
  const [queryParts, setQueryParts] = useState([]);

  useEffect(() => {
    const parts = initialQuery.split(/('(?:''|[^'])*')/);
    setQueryParts(parts.map(part => ({
      text: part,
      editable: /^'.*'$/.test(part),
    })));
  }, [initialQuery]);

  const handleChange = (index, event) => {
    const newQueryParts = [...queryParts];
    newQueryParts[index] = {
      ...newQueryParts[index],
      text: `'${event.target.value}'`,
    };
    setQueryParts(newQueryParts);
  };

  return (
    <div>
      {queryParts.map((part, index) =>
        part.editable ? (
          <TextField
            key={index}
            defaultValue={part.text.slice(1, -1)}
            onChange={(event) => handleChange(index, event)}
          />
        ) : (
          <span key={index}>{part.text}</span>
        )
      )}
    </div>
  );
};

export default SQLQueryEditor
