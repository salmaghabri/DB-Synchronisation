import time

import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


from Product import Product


class DBService:
    def __init__(self, database, host="localhost", user="root", password="", port="3307"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.cursor = self.conn.cursor()

    def create_product_table(self):
        create_query = '''CREATE TABLE IF NOT EXISTS product (
            id INT NOT NULL AUTO_INCREMENT,
            region VARCHAR(30) ,
            product VARCHAR(30),
            total int,
            date DATE,
            PRIMARY KEY (ID)
        ) ;'''
        self.cursor.execute(create_query)
        self.conn.commit()
        print("Product table created successfully")

    def insert_product(self, id,region, product, total, date,bo):
        insert_query = "INSERT INTO product (id,region, product, total, date ,bo) VALUES (%s, %s, %s, %s, %s,%s)"
        values = (id,region, product, total, date ,bo)
        self.cursor.execute(insert_query, values)
        self.conn.commit()
        print("Product inserted successfully")


    def update_product(self, id, region, product, total, date, bo):
        update_query = f"UPDATE `product` SET `region` = '{region}', `product` = '{product}', `total` = '{total}', `date` = '{date}' WHERE `product`.`id` ='{id}' and `product`.`bo` = '{bo}' ;"
        print(update_query)
        self.cursor.execute(update_query)
        self.conn.commit()
        print("Product updated successfully")

    def update_product_up_to_date(self, id,state):
        update_query = f"UPDATE `product` SET `up_to_date` = '{state}' WHERE `product`.`id` ='{id}' ;"
        print(update_query)
        self.cursor.execute(update_query)
        self.conn.commit()
        print("Product up_to_date updated successfully")

    
    def delete_product(self, id):
        print("hiiii")
        delete_query = f"DELETE FROM product WHERE id = '{id}'"
        self.cursor.execute(delete_query)
        self.conn.commit()
        print("Product deleted successfully")

    def getAllProducts(self):
        select_all_query = "SELECT * FROM product"
        products = []
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        for row in rows:
            id, region, product, total, date, up_to_date, bo = row
            p = Product(id, region, product, total, date, up_to_date, bo)
            products.append(p)

        return products

    def RenderTable(self, type):
        font1 = ('Times', 14, 'normal')
        font2 = ('Times', 32, 'bold')
        my_w = tk.Tk()
        my_w.geometry("1000x400")

        my_w.columnconfigure(0, weight=4)
        my_w.columnconfigure(1, weight=2)
        my_w.rowconfigure(0, weight=1)
        my_w.rowconfigure(1, weight=6)
        my_w.rowconfigure(2, weight=2)

        frame_top = tk.Frame(my_w, bg='white')
        frame_bottom = tk.Frame(my_w, bg='white')

        frame_m_right = tk.Frame(my_w, bg='#f8fab4')
        frame_m_right.columnconfigure(0, weight=1)
        frame_m_right.columnconfigure(1, weight=1)
        frame_m_right.columnconfigure(2, weight=1)
        frame_m_right.rowconfigure(0, weight=1)
        frame_m_right.rowconfigure(1, weight=1)
        frame_m_right.rowconfigure(2, weight=1)
        frame_m_right.rowconfigure(3, weight=1)
        frame_m_right.rowconfigure(4, weight=1)
        frame_m_right.rowconfigure(5, weight=1)

        frame_m_left = tk.Frame(my_w, bg='#284474')

        # placing in grid
        frame_top.grid(row=0, column=0, sticky='WENS', columnspan=2)
        frame_m_left.grid(row=1, column=0, sticky='WENS')
        frame_m_right.grid(row=1, column=1, sticky='WENS')
        frame_bottom.grid(row=2, column=0, sticky='WENS', columnspan=2)

        # Layout is over, placing components
        self.table = ttk.Treeview(frame_m_left, selectmode='browse')
        self.table.grid(row=0, column=0, columnspan=2, padx=3, pady=2)
        self.table["columns"] = ("id", "region", "product", "total", "date", "BO")

        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("id", width=50)
        self.table.column("region", width=100)
        self.table.column("product", width=100)
        self.table.column("total", width=50)
        self.table.column("date", width=100)
        self.table.column("BO", width=50)

        self.table.heading("id", text="id")
        self.table.heading("region", text="Region")
        self.table.heading("product", text="Product")
        self.table.heading("total", text="Total")
        self.table.heading("date", text="Date")
        self.table.heading("BO", text="BO")
        # products = self.getAllProducts()
        # for product in products:
        #     self.table.insert("", tk.END, text="",
        #                  values=(product.id,product.region, product.product, product.total, product.date, product.bo))
        
        if "ho_" in type:
            my_w.title('Head Office')
        elif "bo" in type:
            my_w.title("Branch Office " + type[-1])
            lr1 = tk.Label(frame_m_right, text='Region', font=font1)
            lr1.grid(row=0, column=0, sticky='nw')
            region = tk.StringVar()  # string variable for region
            e_region = tk.Entry(frame_m_right, textvariable=region, font=font1)
            e_region.grid(row=0, column=1, columnspan=2)
            self.variables=[]
            product = tk.StringVar()  # string variable for product
            lr2 = tk.Label(frame_m_right, text='Product', font=font1)
            lr2.grid(row=1, column=0, sticky='nw')
            e_product = tk.Entry(frame_m_right, textvariable=product, font=font1)
            e_product.grid(row=1, column=1, columnspan=2)

            total = tk.DoubleVar()  # double variable for price
            lr3 = tk.Label(frame_m_right, text='Total', font=font1)
            lr3.grid(row=2, column=0, sticky='nw')
            e_total = tk.Entry(frame_m_right, textvariable=total, font=font1)
            e_total.grid(row=2, column=1, columnspan=2)

            date = tk.StringVar()  # string variable for product
            lr4 = tk.Label(frame_m_right, text='Date', font=font1)
            lr4.grid(row=3, column=0, sticky='nw')
            e_date = DateEntry(frame_m_right, width=12, background='darkblue',
                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                               textvariable=date)
            e_date.grid(row=3, column=1, columnspan=2)
            insert_button = tk.Button(frame_m_right, text="Insert", font=font1,
                                      command=lambda: self.insertButtonClicked(id.get(),region.get(), product.get(), total.get(),
                                                                               date.get(),type[0]+type[1]))
            id = tk.IntVar()  # double variable for price
            lr4 = tk.Label(frame_m_right, text='id', font=font1)
            lr4.grid(row=4, column=0, sticky='nw')
            e_id = tk.Entry(frame_m_right, textvariable=id, font=font1)
            e_id.grid(row=4, column=1, columnspan=2)
            insert_button.grid(row=5, column=0, padx=20, pady=10)

            self.variables=[id,region,product,total,date]

        #*************buttons***************************
            update_button = tk.Button(frame_m_right, text="Update", font=font1,
                                      command=lambda: self.updateButtonClicked(id.get(),region.get(), product.get(), total.get(),
                                                                               date.get(), type[0]+type[1]))
            update_button.grid(row=5, column=1, padx=20, pady=10)

            # Delete button
            delete_button = tk.Button(frame_m_right, text="Delete", font=font1,
                                      command=lambda: self.deleteButtonClicked(id.get()))

            delete_button.grid(row=5, column=2, padx=20, pady=10)
        def on_select(event):
            self.data_collect()
        self.table.bind("<<TreeviewSelect>>", on_select)
        self.show_items()
        tk.mainloop()


    def show_items(self): # Populating the treeview with records
        for item in self.table.get_children(): # loop all child items 
            self.table.delete(item)        # delete them 
        
        products = self.getAllProducts()
        for product in products:
            self.table.insert("", tk.END, text="",
                            values=(product.id,product.region, product.product, product.total, product.date, product.bo))

    def data_collect(self): # collect data to display for edit
        selected=self.table.focus() # gets the product id or p_id
        values = self.table.item(selected, 'values')
        if(values ):
            print("values of the selected row",values)
            for i,v in enumerate(self.variables):
                v.set(values[i])
                if i==4:
                    break #no form widget for bo

            







    def insertButtonClicked(self,id,region, product, total, date, type):
        self.insert_product(id,region,product,total,date,type)
        self.show_items()


    def updateButtonClicked(self,id, region, product, total,date, type):
        self.update_product_up_to_date(id,"update")
        # time.sleep(10)
        self.update_product(id,region,product,total,date,type)
        self.show_items()

    def deleteButtonClicked(self,id):
        self.update_product_up_to_date(id,"delete")
        time.sleep(10)

        self.delete_product(id)
        self.show_items()



