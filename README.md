# Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

## Project Overview

Cricbuzz LiveStats is a cricket analytics dashboard built using Python, Streamlit, MySQL, and Cricbuzz API data from RapidAPI.

The project fetches cricket match data from the Cricbuzz API, stores it in a MySQL database, and displays cricket insights through an interactive Streamlit dashboard.

## Technologies Used

* Python
* Streamlit
* MySQL
* Pandas
* Requests
* Cricbuzz API via RapidAPI
* SQL

## Features

### 1. Home Page

* Shows project overview
* Displays database summary such as matches, players, venues, series, batting stats, and bowling stats

### 2. Live Matches Page

* Displays recent match details
* Shows teams, venue, city, and match status
* Uses stored Cricbuzz API data from MySQL

### 3. Top Stats Page

* Shows top run scorers
* Shows highest individual scores
* Shows top wicket takers
* Shows bowling economy statistics

### 4. SQL Analytics Page

* Contains 25 SQL queries
* Displays query output directly in Streamlit
* Includes a custom SQL query option

### 5. CRUD Operations Page

* Add player records
* View player records
* Update player details
* Delete player records
* Manually fix missing player data

## Project Folder Structure

```text
CricbuzzLiveStats/
│
├── app.py
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── fetch_matches.py
│   ├── fetch_players.py
│   ├── fetch_scorecards.py
│   ├── fetch_series.py
│   ├── fetch_venues.py
│   ├── save_batting.py
│   ├── save_bowling.py
│   └── test_player.py
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Live_Matches.py
│   ├── 3_Top_Stats.py
│   ├── 4_SQL_Queries.py
│   └── 5_CRUD_Operations.py
│
├── utils/
│   └── db_connection.py
│
└── notebooks/
```

## Database Tables

The MySQL database contains:

* players
* matches
* teams
* venues
* series
* batting_stats
* bowling_stats

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Connection

Database connection is handled in:

```text
utils/db_connection.py
```

Example:

```python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",
        database="cricbuzz"
    )
```

## How to Run

Run this command:

```bash
streamlit run app.py
```

or:

```bash
streamlit run main.py
```

## API Note

Cricbuzz data was fetched using RapidAPI and stored in MySQL.

Due to RapidAPI monthly quota limits, the dashboard displays the latest stored cricket data from the MySQL database.

## SQL Analytics

The SQL Analytics page contains 25 SQL queries covering:

* Player details
* Recent matches
* Top run scorers
* Venue analysis
* Player role count
* Highest scores
* Wicket takers
* Economy rate
* Player performance
* Head-to-head team analysis
* Recent player form
* Quarterly batting trends

## CRUD Operations

The CRUD page allows manual player data management.

It can update:

* Player name
* Country
* Role
* Batting style
* Bowling style

## Conclusion

This project demonstrates API integration, JSON handling, MySQL database management, SQL analytics, CRUD operations, and Streamlit dashboard development using cricket data.
