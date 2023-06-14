import React, { useState } from 'react';
import axios from 'axios';
import {useNavigate} from "react-router-dom"
import { useDispatch } from 'react-redux';
import SearchIcon from '@mui/icons-material/Search';
import { setQuery } from '../state';
import './styles/searchBar.css';

const SearchBar = () => {
  const [query, setQueryInput] = useState('');
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleQuery = async (event) => {
    event.preventDefault();
    
    
    const response = await axios.post('http://localhost:5000/api/query', {
    query: query,
});
if(response.data.query){
    dispatch(setQuery(response.data.query));
  }
    const queryForUrl = query.replace(/ /g, "_");

    navigate(`/ask/${queryForUrl}`);

    console.log(response.data.query)
    console.log(response)

  };

  return (
    <div className="search-bar">
      <form onSubmit={handleQuery}>
        <button type="submit" className="search-button">
          <SearchIcon />
        </button>
        <input
          type="text"
          value={query}
          onChange={(e) => setQueryInput(e.target.value)}
          className="search-input"
          placeholder="Enter your query..."
        />
      </form>
    </div>
  );
};

export default SearchBar;
