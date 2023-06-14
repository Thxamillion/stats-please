import React, { useState, useEffect } from 'react';
import { Box } from "@mui/material";
import StatsTable from '../../components/statsTable';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import Navbar from '../../components/navbar';
import Billboard from '../../components/billboard';

const ResultPage = () => {
    const [results, setResults] = useState([]);
    const [encodedSQLQuery, setEncodedSQLQuery] = useState('');
    const sqlQuery = useSelector(state => state.query);  
    const { user_query } = useParams();
    const query = user_query.replace(/_/g, ' ');
    
    useEffect(() => {
        const fetchResults = async () => {
            try {
                let finalEncodedSQLQuery = '';

                if (sqlQuery) {
                    finalEncodedSQLQuery = encodeURIComponent(sqlQuery.substring(sqlQuery.indexOf("SELECT")));
                } else {
                    const response = await fetch('http://localhost:5000/api/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query }),
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    } else {
                        const data = await response.json();
                        const responseText = data.query;
                        const extractedQuery = responseText.substring(responseText.indexOf("SELECT"));
                        finalEncodedSQLQuery = encodeURIComponent(extractedQuery);
                    }
                }

                const response = await fetch(`http://localhost:5000/api/results?query=${finalEncodedSQLQuery}`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                } else {
                    const data = await response.json();
                    setResults(data.results);
                }
            } catch (error) {
                console.error(error);
                // Handle error
            }
        };
    
        fetchResults();
    }, [query, sqlQuery]);

    return (
        <Box>
            <Navbar/>
            <Billboard query={query} sqlQuery={sqlQuery}/>
            <StatsTable data={results} sqlQuery={sqlQuery} />
        </Box>
    );
}

export default ResultPage;
