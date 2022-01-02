import pymysql as mysql

def connection():
    db=mysql.connect(host="localhost",user="root",password="1234",port=3306,db="restro_db")
    cmd=db.cursor()
    return db,cmd


  