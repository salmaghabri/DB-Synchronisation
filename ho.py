import json
import threading
import time
import pika
import tkinter as tk
from tkinter import ttk

from db import DBService
from Product import Product;


# QUEUE_NAME = "bo"

frame = tk.Tk()
frame.title("Head Office")
table = ttk.Treeview(frame)
<<<<<<< HEAD
db_service = DBService("localhost", "root" , "", "ho",3307)
=======
db_service = DBService("localhost", "root" , "", "ho",3306)
>>>>>>> d4f50bf (ah bon)
def main():
    # UI

    table["columns"] = ("region", "product", "total", "date", "BO")

    table.column("#0", width=0, stretch=tk.NO)
    table.column("region", width=100)
    table.column("product", width=100)
    table.column("total", width=50)
    table.column("date", width=100)
    table.column("BO", width=50)

    table.heading("region", text="Region")
    table.heading("product", text="Product")
    table.heading("total", text="Total")
    table.heading("date", text="Date")
    table.heading("BO", text="BO")

    table.pack()
    start_consumer_thread()
    for product in db_service.getAllProducts():
        table.insert("", tk.END, text="",
                     values=(product.region, product.product, product.total, product.date, product.bo))
    tk.mainloop()



    # channel1.start_consuming()

def start_consumer_thread():
    consumer_thread1 = threading.Thread(target=consume,args=("bo1",))
    consumer_thread2 = threading.Thread(target=consume,args=("bo2",))
    consumer_thread1.start()
    consumer_thread2.start()

def consume(QUEUE_NAME):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel1 = connection.channel()
    # channel2 = connection.channel()
    channel1.queue_declare(queue=QUEUE_NAME)
    # channel1.queue_declare(queue=QUEUE_NAME + str(2))
    print(f" [*] Waiting for messages in {QUEUE_NAME}")

    def callback(ch, method, properties, body):
        received_message = body.decode('utf-8')
        print(received_message)
        p = deserialize(received_message)
        p=Product(p['id'],p['region'],p['product'],p['total'],p['date'],p['up_to_date'] ,method.routing_key)
        # print(p)
        try:
            if p.up_to_date == "add":
                print(p.up_to_date)
                print(method.routing_key)
                db_service.insert_product(p.id,p.region, p.product, p.total, p.date,method.routing_key)
                table.insert("", tk.END, text="",
                             values=(p.region, p.product, p.total, p.date, method.routing_key),tags=("add",))
                table.tag_configure("add", background="green")
                table.update()
            elif p.up_to_date == "update":
                db_service.update_product(p.id, p.region, p.product, p.total, p.date,p.bo)
                
                for item in table.get_children():
                    values = table.item(item, 'values')
                    if values[0] == p.region:  
                        print(values[0])
                        table.item(item, values=(p.region, p.product, p.total, p.date),tags=("update",))
                        table.tag_configure("update", background="yellow")
                table.update()
                
            elif p.up_to_date == "delete":
                # print("salut")
                db_service.delete_product(p.id)
                for item in table.get_children():
                    values = table.item(item, 'values')
                    if values[0] == p.region:  
                        print(values[0])
                        table.item(item, values=(p.region, p.product, p.total, p.date),tags=("delete",))
                        table.tag_configure("delete", background="red")
                        time.sleep(3)
                        table.delete(item) 


                table.update()


        except Exception as e:
            print(str(e))

    channel1.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    channel1.start_consuming()
def deserialize(message):
    return json.loads(message)

def worker():
        table.update()



if __name__ == '__main__':
    # render_thread = threading.Thread(target=worker)
    main()
    # tk.mainloop()