import React, { useEffect, useState } from 'react'
import { data, useParams } from 'react-router-dom'
import { getCorrelationData } from '../services/api'
import DatePicker from "react-datepicker";
import * as d3 from 'd3'
import "react-datepicker/dist/react-datepicker.css";
import "./css/correlation.css"
function CorrelationPage() {
  const today = new Date()
  const correctToday = new Intl.DateTimeFormat('en-CA').format(today);
  const yesterday = new Date(today)
  yesterday.setDate(today.getDate() - 30)
  const correctYesterday = new Intl.DateTimeFormat('en-CA').format(yesterday);

  const [company, setCompany] = useState("TSLA");
  const [correlationData, setCorrelationData] = useState(null);
  const [startDate, setStartDate] = useState(correctYesterday)
  const [endDate, setEndDate] = useState(correctToday)

  // setting the margins and dimensions of the graph
  var margin = { top: 10, right: 100, bottom: 30, left: 30 },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;



  // append the svg object to the body of the page
  useEffect(() => {
    if (!company){
      return
    }
    async function fetchData() {
      const data = await getCorrelationData(company, startDate, endDate);
      setCorrelationData(data)

    }
    const allGroup = ["TSLA", "MSFT", "APPL"];

    d3.select("#RAI_correlation").selectAll("*").remove();
    d3.select("#stock-chart").selectAll("*").remove();
    
d3.select("#RAI_correlation").select("svg").remove();
d3.select("#stock-chart").select("svg").remove();
d3.select("#sentiment-chart").select("svg").remove();
    // Clear and create dropdown
 

    fetchData();
  }, [startDate, endDate, company])


  useEffect(() => {

    if (!correlationData || typeof correlationData['0'] === 'undefined') {
      return;
    }

    // Clear old chart
    d3.select("#RAI_correlation").selectAll("*").remove();
    d3.select("#stock-chart").selectAll("*").remove();
    d3.select("#sentiment-chart").selectAll("*").remove();
    const data = correlationData['0'][5][0]
    const dateData = correlationData['0'][5][0]['date']
    const RAIData = Object.values(correlationData['0'][5][0]['RedditActivityIndex']).flat()
    const openData = Object.values(correlationData['0'][5][0]['open'])
    const sentimentData = Object.values(data.Sentiment_Score).map(d => +parseFloat(d));
    const allDates = Object.values(dateData).flat();
    const indices = Object.keys(data.date)
    const dataArray = indices.map(i => {
      const entry = {};
      for (const key in data) {
        entry[key] = data[key][i];
      }
      return entry
    })

    console.log(dataArray)
    console.log(sentimentData)




    const margin = { top: 10, right: 100, bottom: 30, left: 30 },
      width = 460 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;

    //create sentiment correlation svg
    const svg = d3.select("#RAI_correlation")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
      svg.append("text")
      .attr("class","title")
      .attr("x", width/2)
      .attr("y",margin.top)
      .attr("font-family","sans-serif")
      .attr("fill","black")
      .attr("text-anchor","middle")
      .text("RAI")

    //create stock svg
    const stock_svg = d3.select("#stock-chart")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + ',' + margin.top + ")")

      stock_svg.append("text")
      .attr("class","title")
      .attr("x", width/2)
      .attr("y",margin.top)
      .attr("font-family","sans-serif")
      .attr("fill","black")
      .attr("text-anchor","middle")
      .text("Stock")


    const sentiment_svg = d3.select("#sentiment-chart")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + ',' + margin.top + ")")

      sentiment_svg.append("text")
      .attr("class","title")
      .attr("x", width/2)
      .attr("y",margin.top)
      .attr("font-family","sans-serif")
      .attr("fill","black")
      .attr("text-anchor","middle")
      .text("Sentiment")


    // Load CSV and build chart

    const allGroup = ["TSLA", "MSFT", "APPL"];



    const myColor = d3.scaleOrdinal()
      .domain(allGroup)
      .range(d3.schemeSet2);

    const x = d3.scaleTime()
      .domain(d3.extent(allDates, d => new Date(d)))
      .range([0, width]);

    //create x axis for sentiment correlation data
    svg.append("g")
    .attr("class", "x-axis")
    .attr("transform", "translate(0," + height + ")")
    .call(
      d3.axisBottom(x)
        .ticks(6) // limit number of ticks (optional)
        .tickFormat(d3.timeFormat("%b %d")) // e.g. "Apr 11"
    );
    //create x axis for stock data
    stock_svg.append("g")
    .attr("class", "x-axis")
    .attr("transform", "translate(0," + height + ")")
    .call(
      d3.axisBottom(x)
        .ticks(6) // limit number of ticks (optional)
        .tickFormat(d3.timeFormat("%b %d")) // e.g. "Apr 11"
    );

    sentiment_svg.append("g")
  .attr("class", "x-axis")
  .attr("transform", "translate(0," + height + ")")
  .call(
    d3.axisBottom(x)
      .ticks(6) // limit number of ticks (optional)
      .tickFormat(d3.timeFormat("%b %d")) // e.g. "Apr 11"
  );

    const y = d3.scaleLinear()
      .domain([d3.min(RAIData), d3.max(RAIData)])
      .range([height, 0]);
    svg.append("g").call(d3.axisRight(y));


    const y_stock = d3.scaleLinear()
      .domain([d3.min(openData), d3.max(openData)])
      .range([height, 0]);
    stock_svg.append("g").call(d3.axisRight(y_stock));

    const y_sentiment = d3.scaleLinear()
      .domain([d3.min(sentimentData), d3.max(sentimentData)])
      .range([height, 0]);


    sentiment_svg.append("g").call(d3.axisRight(y_sentiment));

    const scatterPlot = svg.append('g')
      .selectAll("circle")
      .data(dataArray)
      .enter()
      .append("circle")
      .attr("cx", d => x(new Date(d.date)))
      .attr("cy", d => y(+parseInt(d.RedditActivityIndex)))
      .attr("r", 4)
      .attr("fill", "blue")

    const stockScatterPlot = stock_svg.append("g")
      .selectAll("circle")
      .data(dataArray)
      .enter()
      .append("circle")
      .attr("cx", d => x(new Date(d.date)))
      .attr("cy", d => y_stock(+parseInt(d.open)))
      .attr("r", 4)
      .attr("fill", "blue")


    const sentimentScatterPlot = sentiment_svg.append("g")
      .selectAll("circle")
      .data(dataArray)
      .enter()
      .append("circle")
      .attr("cx", d => x(new Date(d.date)))
      .attr("cy", d => y_sentiment(+parseFloat(d.Sentiment_Score)))
      .attr("r", 4)
      .attr("fill", "blue")





    function update(selectedGroup) {
      const dataFilter = dataArray.map(d => ({
        date: d.date,
        RedditActivityIndex: d.RedditActivityIndex,
      }));

      scatterPlot.join(
        enter => enter.append("circle")
          .attr("cx", d => x(new Date(d.date)))
          .attr("cy", d => y(+parseFloat(d.RedditActivityIndex)))
          .attr("r", 0)
          .attr("fill", "blue")
          .transition().duration(1000)
          .attr("r", 4),

        update => update
          .transition().duration(1000)
          .attr("cx", d => x(new Date(d.date)))
          .attr("cy", d => y(+parseFloat(d.RedditActivityIndex)))
          .attr("r", 4),

        exit => exit
          .transition().duration(500)
          .attr("r", 0)
          .remove()
      );
    }
    d3.select("#selectButton").on("change", function () {
      const selectedOption = d3.select(this).property("value");
      update(selectedOption);
    });

  }, [correlationData, startDate, endDate,company]); // Only runs once on mount




  function setStart(start) {
    setStartDate(new Intl.DateTimeFormat('en-CA').format(start))

  }
  function setEnd(end) {
    setEndDate(new Intl.DateTimeFormat('en-CA').format(end))
  }

  function setSelectedCompany(e){
    console.log(e)
    var companySelected = e.target.value;
    setCompany(companySelected)
    console.log(companySelected)
  }


  return (

    <div>
      <link rel="stylesheet" href="correlation.css"></link>

      <p>Correlation Page</p>
      <p>Reddit Data for {company}</p>
      <div>


        
          <div className='main'>
          <div className='main-chart'>
            <div className='container' id="stock-chart"></div>
           
            <select name="companies" id="companies" onChange={(e)=>setSelectedCompany(e)}>
              <option value="TSLA">Tesla</option>
              <option value="MSFT">Microsoft</option>
              <option value="APPL">Apple</option>
            </select>
            {console.log()}
            
            </div>
            <div className='Dates'>
          <DatePicker selected={startDate} onChange={(startDate) => setStart(startDate)} />
        
        <DatePicker selected={endDate} onChange={(endDate) => setEnd(endDate)} />
      </div>
      </div>
      

      
          </div>
          <div className='default-charts'>
          <div className="container" id="RAI_correlation"></div>
          <div className='container' id="sentiment-chart"></div>

          </div>

       
        

      {correlationData ? (correlationData['0']? console.log(correlationData['0']):
      <p>There was no data for this company between the given dates</p>):<p>Waiting</p>
      
    
    }

      
    </div>
  )
}

export default CorrelationPage;