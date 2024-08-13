import sqlite3
from datetime import datetime
import json


def db_dump(myparams, results):
    # Connect to SQLite database/ create it if it doesn't exis
    conn = sqlite3.connect("sim_results.db")
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS simulations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        params TEXT,
        result TEXT
    )
    """
    )

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert the params dictionary and simulation result to JSON strings
    params_json = json.dumps(myparams)
    result_json = json.dumps(results)  # Adjust this based on `sim`'s structure

    # Insert the data into the table
    cursor.execute(
        """
    INSERT INTO simulations (timestamp, params, result)
    VALUES (?, ?, ?)
    """,
        (timestamp, params_json, result_json),
    )

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


def db_clear():
    # Connect to the SQLite database
    conn = sqlite3.connect("sim_results.db")
    cursor = conn.cursor()

    # Delete all rows from the simulations table
    cursor.execute("DELETE FROM simulations")

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
