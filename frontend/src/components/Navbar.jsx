import React from 'react'
import {Link} from 'react-router-dom';


function Navbar(){
    return(
        <nav>
            <Link to ='/'>Home</Link>
            <Link to ='/stock/TSLA'>Stock</Link>
            <Link to ='/reddit/TSLA'>Reddit</Link>
            <Link to ='/correlation'>Correlation</Link>


        </nav>
    )
}

export default Navbar;