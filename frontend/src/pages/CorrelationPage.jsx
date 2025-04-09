import React, { useEffect, useState } from 'react'
import {useParams} from 'react-router-dom'
import { getCorrelationData } from '../services/api'
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";
function CorrelationPage(){
    const {ticker} = useParams();
    const [correlationData, setCorrelationData] = useState(null);
    const [startDate,setStartDate] = useState(null)
    const [endDate,setEndDate] = useState(null)
    useEffect(()=>{
        async function fetchData(){
            const data = await getCorrelationData(ticker,startDate,endDate);
            setCorrelationData(data)
            console.log('recieved!',Object.values(data))
        }
        fetchData();
    },[ticker])
    return(
        <div>
            <p>Correlation Page</p>
            <p>Reddit Data for {ticker}</p>
              <div> 
                <div>

                <DatePicker selected={startDate} on onChange={(startDate)=> setStartDate(startDate)}/>
                </div>
                <DatePicker selected={endDate} on onChange={(endDate)=> setEndDate(endDate)}/>
                    </div>
            {console.log("Test",correlationData)}
            {console.log(startDate)}
            {console.log(endDate)}
            {correlationData?(<div><p>Data Successfully Aquired!</p>
            <p>{Array.from(correlationData)}</p>
            
            
            </div>):(<p>Loading data ...</p>)}
        </div>
    )
}

export default CorrelationPage;