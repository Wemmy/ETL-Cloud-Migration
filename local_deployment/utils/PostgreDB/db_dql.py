from db_connect import *
import pandas as pd

def fetch_data(conn, query):
    """
    Fetch data from PostgreSQL database and return it as a Pandas DataFrame.
    
    :param conn: Database connection object
    :param query: SQL query string
    :return: DataFrame containing the query results
    """
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    conn = create_connection(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_NAME)

    query = '''
    select * from stock;
    '''
    df = fetch_data(conn, query)
    
    # pivot table 
    pivoted_df = df.pivot(index='date', columns='ticker', values='adj_close')
    print(pivoted_df.head())
    