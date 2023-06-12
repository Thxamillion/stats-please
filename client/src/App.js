import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState("");
  const [sqlQuery, setSqlQuery] = useState("");

  const getQuery = async () => {
    const response = await axios.post('http://localhost:5000/api/query', { query: query });
    setSqlQuery(response.data.query);
    console.log(sqlQuery)
  }

  return (
    <div className="App">
      <input type="text" value={query} onChange={e => setQuery(e.target.value)} />
      <button onClick={getQuery}>Generate SQL Query</button>
      {sqlQuery && <p>{sqlQuery}</p>}
    </div>
  );
}

export default App;
