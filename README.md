
# 🧠 Sentiment-Stock Flask API Deployment Overview

## 📦 Project Structure

This Flask API exposes endpoints for sentiment and volatility analysis of S&P 500 stocks.

## 🧱 Backend Architecture

- Built using **Flask + Blueprints** for modular routing
- Routes:
  - `/api/stock/<ticker>` – returns stock price data + volatility
  - `/api/reddit/<ticker>` – returns Reddit sentiment and activity metrics
  - `/api/correlation/<ticker>` – combines and compares Reddit vs stock data
- Each route delegates logic to a corresponding function inside a **`services/`** folder

## 🧠 Services Layer

- `reddit_service.py` – simulates Reddit sentiment & virality scoring
- `stock_service.py` – simulates stock volatility using dummy historical prices
- `correlation_service.py` – combines outputs from both and calculates basic correlation
- Each service will later be upgraded to pull real-time data

## 🚀 Deployment

Deployed to an **AWS EC2 instance** running **Ubuntu 24.04**.

### Steps:
1. Cloned the project repo to the server
2. Created a **Python virtual environment** using `venv`
3. Installed dependencies from `requirements.txt`
4. Used **Gunicorn** to run the Flask app on `localhost:8000`:
   ```bash
   gunicorn -w 4 -b 127.0.0.1:8000 run:app
   ```

## 🌐 Reverse Proxy with NGINX

NGINX was installed and configured to:
- Accept public traffic on port 80
- Forward requests to Gunicorn on `localhost:8000`
- Handle domain routing (`api.mydomain.com`) via A record

### Sample NGINX Config:
```nginx
server {
    listen 80;
    server_name api.mydomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔐 SSL / HTTPS

Used **Certbot** with Let’s Encrypt to enable HTTPS:
```bash
sudo certbot --nginx -d api.mydomain.com
```
Certbot auto-updated the NGINX config and redirects HTTP to HTTPS.

---
