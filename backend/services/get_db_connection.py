import os
import sqlite3


def get_db_conn():
    '''Method to connect with the sqlite database with the given name.

       :returns: Returns connection object or exception it it fails. 
    '''
    try:
        database_path = os.path.join(os.getcwd(), 'database/transactions.db') 
        c = sqlite3.connect(database_path)
        connection = c.cursor()
        table_name = 'furniture'
        connection.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = connection.fetchone()
        
        if result is None:
            connection.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                transaction_hash TEXT PRIMARY KEY,
                                block_number INTEGER,
                                timestamp INTEGER,
                                sender TEXT,
                                receiver TEXT,
                                value TEXT,
                                gas_price TEXT,
                                gas_limit TEXT,
                                nonce INTEGER,
                                status INTEGER
                            );''')
            return c
        else:
            return c
    
    except Exception as e:
        print(e)