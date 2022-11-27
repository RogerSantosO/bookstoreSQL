import pyodbc
import pandas as pd
import mysql.connector
# insert data from csv file into dataframe.
# working directory for csv file: type "pwd" in Azure Data Studio or Linux
# working directory in Windows c:\users\username
df = pd.read_csv("books.csv")
passw = open('password.txt','r')
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'localhost' 
database = 'BOOKSTORE' 
username = 'admin_user' 
password = passw.read()
cnxn = mysql.connector.connect(host='localhost',database='BOOKSTORE',user='admin_user',password=passw.read())
cursor = cnxn.cursor()
# Insert Dataframe into SQL Server:
for index, row in df.iterrows():
    cursor.execute(f"""INSERT INTO BOOKSTORE.Books (Nome_livro,Categoria,Estrelas,Preco,Estoque) VALUES("{row.livro}","{row.categoria}",{row.estrelas},{row.preco},{row.estoque})""")
cnxn.commit()
cursor.close()