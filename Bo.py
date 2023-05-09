import json
import threading
import mysql.connector
import pika
import time

from Product import Product
from DBService import DBService;

class Bo:
    def __init__(self,id) -> None:
        self.id=id
        self.name=f'bo{id}'
        self.mydb=DBService(self.name)

    def connectDB(self):
        self.mydb=DBService(self.name)


    def connectMQ(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.name)

        self.channel.confirm_delivery()

    def start_polling(self):
        poll_thread = threading.Thread(target=self.poll)
        poll_thread.start()
    def poll(self):
        while True:
            self.polling_func()
            time.sleep(5)

    def polling_func(self):
        self.connectDB()
        mycursor = self.mydb.cursor
        print("looking for updates...")
        ps=self.get_products_to_send(mycursor)
        for p in ps:
            json_date = p.get_date().strftime('%Y-%m-%d')
            p.set_date(json_date)
            
            try:
                self.channel.basic_publish(exchange='', routing_key=self.name, body=json.dumps(p.__dict__))
                print(f'product of id { p.get_id()} sent ')
                p.set_up_to_date('ok')
                mycursor.execute(f"UPDATE product SET up_to_date ='ok'  where id= '{ p.get_id()}' " )
                self.mydb.conn.commit()
            except pika.exceptions.UnroutableError:
                print('Message could not be confirmed')

    def get_products_to_send(self,mycursor):
        select_to_send=f"select * from product where up_to_date <> 'ok'  "
        products=[]
        mycursor.execute(select_to_send)
        rows=mycursor.fetchall()
        for row in rows: 
            id,region,product,total,date,up_to_date,bo= row
            p=Product(id,region,product,total,date,up_to_date,bo)
            products.append(p)
            print(p)
        return products

    



    def gui(self):
        self.mydb.RenderTable(["bo", str(self.id)])


    