import pandas as pd
import sqlite3
from sqlalchemy import create_engine

conn = sqlite3.connect("products.db")
disk_engine = create_engine('sqlite:///products.db')
c = conn.cursor()

def read():
    df = pd.read_sql_query("select * from laptops;", conn)
    return df

def write_data_to_database(df):

    #Adding Timestamp
    df['datetime'] = pd.Timestamp("today").strftime("%m/%d/%Y")

    # Appending the results to lazada_producct
    df.to_sql('laptops', disk_engine, if_exists='append')

def data_cleansing(df):
	new_df = df.copy()
	product_name = new_df["product_name"]
	product_name = product_name.apply(lambda x: x.split()[2:])
	product_name = product_name.apply(lambda x: ' '.join(x))
	new_df["product_name"] = product_name

	return new_df