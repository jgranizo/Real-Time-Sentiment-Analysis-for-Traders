import axios from 'axios'


const API_BASE_URL = "https://sentimentapi.jeremygranizo.tech/api/";

export const getStockData = async (ticker) =>{
    try {
        const response = await axios.get(`${API_BASE_URL}stock/${ticker}`)
        return response.data
    }
    catch(error){
        console.error("Error fetching stock data: ", error)
        return null
    }
}

export const getRedditData = async (ticker) =>{
    try {
        const response = await axios.get(`${API_BASE_URL}reddit/${ticker}`)
        console.log(response.data)
        return response.data
    }
    catch(error){
        console.error("Error fetching reddit data: ", error)
        return null;
    }
}

export const getCorrelationData = async (ticker) =>{
    try {
        const response = await axios.get(`${API_BASE_URL}/api/correlation/${ticker}`)

        return response.data
    }
    catch(error){
        console.error("Error fetching correlation data: ", error)
        return null;
    }
}