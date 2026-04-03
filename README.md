This project is vibe coded and was aimed to explore vibe-coding
 💳 Transaction Analytics

A Streamlit web app to explore and analyze personal transaction data by merchant and date range.

## Features

- Filter transactions by merchant and date range
- View total spent, total earned, and net balance per merchant
- Powered by DuckDB for fast in-memory SQL queries
- Uses Supabase as the primary data source, with automatic fallback to a local Excel file if Supabase is offline

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [DuckDB](https://duckdb.org/) — in-memory SQL engine
- [Supabase](https://supabase.com/) — cloud database
- [Pandas](https://pandas.pydata.org/) — data manipulation

## Setup

### 1. Clone the repo

bash
git clone https://github.com/chef-ts-glitch/transactions-app.git
cd transactions-app


### 2. Create a virtual environment and install dependencies

bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### 3. Add Supabase credentials

Create a .streamlit/secrets.toml file:

toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-key"


### 4. Run the app

bash
streamlit run app.py


## Data Fallback

If Supabase is unreachable, the app automatically falls back to reading from 'transactions.xlsx' in the project root.

