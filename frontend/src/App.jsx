import React from 'react';
import {BrowserRouter as Router,Routes, Route} from 'react-router-dom'
import Home from './pages/Home';
import StockPage from './pages/StockPage';
import RedditPage from './pages/RedditPage';
import CorrelationPage from './pages/correlationPage'


function App() {
    return (
        <Router>
            <Routes>
                <Route path='/' element={<Home></Home>}></Route>
                <Route path='/stock/:ticker' element={<StockPage></StockPage>}></Route>
                <Route path='/reddit/:ticker' element={<RedditPage></RedditPage>}></Route>
                <Route path='/correlation/:ticker' element={<CorrelationPage></CorrelationPage>}></Route>

            </Routes>
        </Router>
    )
}

export default App;