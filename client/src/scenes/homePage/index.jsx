import { useEffect, useState } from 'react';
import SearchBar from "../../components/searchBar";
import { useSelector } from 'react-redux';
import Navbar from "../../components/navbar";
import { Box } from "@mui/material";

const HomePage = () => {
  const loading = useSelector(state => state.query.loading);
  const [dotCount, setDotCount] = useState(0);

  useEffect(() => {
    let intervalId;

    if (loading) {
      intervalId = setInterval(() => {
        setDotCount((prevCount) => (prevCount + 1) % 4);
      }, 500);
    }

    return () => clearInterval(intervalId);
  }, [loading]);

  return (
    <Box>
      <Navbar />
      <SearchBar />
      {loading && <p>Retrieving stats{'.'.repeat(dotCount)}</p>}
    </Box>
  );
}

export default HomePage;

