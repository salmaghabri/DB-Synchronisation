import json
import mysql.connector
import pika
import schedule
import time
from Product import Product

def getAllProducts():
    select_all_query="select * from product"
    products=[]
    mycursor.execute(select_all_query)
    rows=mycursor.fetchall()
    for row in rows: 
        id,region,product,total,date,up_to_date= row
        p=Product(id,region,product,total,date,up_to_date)
        products.append(p)

    return products



def get_products_to_send():
    select_to_send=f"select * from product where up_to_date <> 'ok'  "
    products=[]
    mycursor.execute(select_to_send)
    rows=mycursor.fetchall()
    for row in rows: 
        id,region,product,total,date,up_to_date, bo= row
        p=Product(id,region,product,total,date,up_to_date,bo)
        products.append(p)
    return products
    


db_host = "localhost"
db_user = "root"
db_name = "bo2"
db_pass = "root"
mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    database=db_name,
    port= "3307",
)
mycursor = mydb.cursor()



#conncet to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='bo2')



#polling function
def polling_func():
    print("polling function running...")
    ps=get_products_to_send()
    for p in ps:
        json_date = p.get_date().strftime('%Y-%m-%d')
        p.set_date(json_date)
        channel.basic_publish(exchange='', routing_key='bo2', body=json.dumps(p.__dict__))
        print(f'product of id { p.get_id()} sent ')
        p.set_up_to_date('ok')
        mycursor.execute(f"UPDATE product SET up_to_date ='ok'  where id= { p.get_id()}" )
        mydb.commit()


while True:
    polling_func()
    time.sleep(10)

