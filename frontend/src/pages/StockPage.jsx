import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom'
import { getStockData } from '../services/api';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function StockPage(){
    const {ticker} = useParams();
    const [stockData,setStockData] = useState(null);

    useEffect(() =>{
        async function fetchData(){
            const data = await getStockData(ticker);
            setStockData(data);
        }
        fetchData();
    },[ticker]);


    return(
        <div>
            <h1>Stock Data for {ticker}</h1>
            {stockData?(
                <Line 
                data={{labels: stockData.price_series.map((_,index)=> `Day ${index+1}`),
                    datasets:[
                    {
                        label:'Stock Price',
                    data:stockData.price_series,
                    borderColor: 'rgba(75,192,192,1)',
                    borderWidth:2,
                    fill:false,
                },
            ]  ,
        }}/>
            ):(<p>Loading data...</p>)}
        </div>
    );
}
export default StockPage