import React, { useEffect, useState } from 'react'
import {useParams} from 'react-router-dom'
import { getCorrelationData } from '../services/api'
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";
function CorrelationPage(){
    const today = new Date()
    const correctToday = new Intl.DateTimeFormat('en-CA').format(today);
    const yesterday = new Date(today)
    yesterday.setDate(today.getDate()-1)
    const correctYesterday = new Intl.DateTimeFormat('en-CA').format(yesterday);
    const {ticker} = useParams();
    const [correlationData, setCorrelationData] = useState(null);
    const [startDate,setStartDate] = useState(correctYesterday)
    const [endDate,setEndDate] = useState(correctToday)
    useEffect(()=>{
        async function fetchData(){
            const data = await getCorrelationData(ticker,startDate,endDate);
            setCorrelationData(data)
            
        }
        
        fetchData();
    },[endDate])

        function setStart(start){
                setStartDate( new Intl.DateTimeFormat('en-CA').format(start))
              
    }
    function setEnd(end){
        setEndDate( new Intl.DateTimeFormat('en-CA').format(end))
    }

    return(
        <div>
            <p>Correlation Page</p>
            <p>Reddit Data for {ticker}</p>
              <div> 
                <div>

                <DatePicker selected={startDate} onChange={(startDate)=> setStart(startDate)}/>
                </div>
                <DatePicker selected={endDate} onChange={(endDate)=> setEnd(endDate)}/>

                    </div>
           
            {correlationData?(<div><p>Data Successfully Aquired!</p>
            <p>{console.log(correlationData)}</p>
            
            
            </div>):(<p>Loading data ...</p>)}
        </div>
    )
}

export default CorrelationPage;