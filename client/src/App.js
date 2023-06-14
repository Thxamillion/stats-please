import React, { useState } from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import HomePage from './scenes/homePage';
import ResultPage from './scenes/resultsPage';
import store from './state/index.js'

function App() {
  

  return <div className='app'>
    <Provider store={store}>
    <BrowserRouter>
    <Routes>
      
        
        <Route path="/ask" 
        element={<HomePage/>} />
        <Route path="/ask/:user_query" 
        element={<ResultPage/>} />

    </Routes>
    </BrowserRouter>
    </Provider>
    </div>
}

export default App;
