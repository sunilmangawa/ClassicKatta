# import the modules
from pymysql import*
import xlwt
import pandas.io.sql as sql
# connect the mysql with the python
con=connect(user="coder",password="@Work/Minute",host="localhost",database="classicmill1")
# read the data
df=sql.read_sql('select * from cm1kattatable',con)
# print the data
print(df)
# export the data into the excel sheet
df.to_excel('katta_dbexcel.xlsx')
