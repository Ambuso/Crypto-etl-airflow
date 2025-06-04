from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

default_args = {
    'owner': 'Ambuso',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 20),
    'email': ['dismasmik3@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

coin_list = [
    'bitcoin', 'ethereum', 'tether', 'xrp', 'binancecoin',
    'solana', 'usd-coin', 'dogecoin', 'cardano', 'tron',
    'avalanche-2', 'polkadot', 'chainlink', 'litecoin', 'stellar'
]

def fetch_and_store_crypto_prices():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'ids': ','.join(coin_list),
        'vs_currency': 'usd'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch data from API: {e}")
        return

    data = response.json()
    rows = []
    timestamp = datetime.utcnow()

    for coin in data:
        rows.append((
            coin['name'],
            coin['symbol'].upper(),
            coin['current_price'],
            coin['market_cap'],
            coin['total_volume'],
            timestamp
        ))

    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
            
        )
        cursor = conn.cursor()

        cursor.execute("CREATE SCHEMA IF NOT EXISTS crypto;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crypto.crypto_prices (
                name TEXT,
                symbol TEXT,
                price NUMERIC,
                market_cap NUMERIC,
                total_volume NUMERIC,
                timestamp TIMESTAMP
            );
        """)

        insert_query = """
            INSERT INTO crypto.crypto_prices (name, symbol, price, market_cap, total_volume, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        for row in rows:
            cursor.execute(insert_query, row)

        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

with DAG(
    dag_id='coin_price_etl_dag',
    default_args=default_args,
    description='Fetch and store hourly crypto prices from CoinGecko',
    schedule_interval='@hourly',
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_and_store_crypto_prices',
        python_callable=fetch_and_store_crypto_prices,
    )
