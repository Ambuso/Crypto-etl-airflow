# 🪙 Crypto Price ETL Pipeline with Apache Airflow

This project is an ETL (Extract, Transform, Load) pipeline built using **Apache Airflow**. It fetches real-time cryptocurrency market data from the **CoinGecko API** on an hourly basis and stores it in a **PostgreSQL** database.

---

## 📌 Features

- Extracts data for 15 major cryptocurrencies including Bitcoin, Ethereum, Solana, etc.
- Loads market price, market cap, and total volume into a PostgreSQL database.
- Scheduled to run hourly using Airflow.
- Stores data in a structured time-series table under the `crypto` schema.
- Supports retry logic and error handling.
- Uses a `.env` file to securely manage sensitive database credentials.

---

## 📦 Tech Stack

- **Apache Airflow**
- **Python 3.12**
- **CoinGecko API**
- **PostgreSQL**
- **psycopg2**
- **python-dotenv**

---

## 🔧 Setup Instructions
1. Clone the Repository

git clone https://github.com/your-username/crypto-price-pipeline.git
cd crypto-price-pipeline

2. Create a Python Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt

4. Set Up Environment Variables
Create a .env file in the root directory with the following contents:
DB_NAME=defaultdb
DB_HOST=your-db-host.aivencloud.com
DB_USER=avnadmin
DB_PASSWORD=yourpassword
DB_PORT=17440

5. Initialize and Start Airflow
# Set Airflow home
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize database
airflow db init

# Start webserver and scheduler
airflow webserver --port 8080
airflow scheduler

🧪 Testing the DAG
Go to http://localhost:8080 in your browser.

Enable the DAG named coin_price_etl_dag.

Trigger it manually or wait for the next scheduled run.

Check the logs to ensure data is fetched and stored correctly.

📊 Output
Data is stored in a PostgreSQL table named:
crypto.crypto_prices
| name    | symbol | price | market\_cap | total\_volume | timestamp           |
| ------- | ------ | ----- | ----------- | ------------- | ------------------- |
| Bitcoin | BTC    | ...   | ...         | ...           | 2025-06-04 10:00:00 |

🤝 Contributing
Feel free to fork the repo and submit PRs. Feedback and feature suggestions are welcome!

📫 Contact
Author: Ambuso Dismas
📧 Email: dismasmik3@gmail.com

📝 License
This project is licensed under the MIT License.


