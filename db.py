import mysql.connector
from Product import Product



class DBService:
    def __init__(self, host, user, password, database, port):
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
        



    def insert_product(self,id, region, product, total, date,bo):
        insert_query = "INSERT INTO product (id,region, product, total, date ,bo) VALUES (%s,%s, %s, %s, %s, %s)"
        values = (id,region, product, total, date ,bo)
        self.cursor.execute(insert_query, values)
        self.conn.commit()
        print("Product inserted successfully")

    def update_product(self, id,region, product, total, date, bo):
        update_query = f"UPDATE `product` SET `region` = '{region}', `product` = '{product}', `total` = '{total}', `date` = '{date}' WHERE `product`.`id` ='{id}' and `product`.`bo` = '{bo}' ;"
        
        self.cursor.execute(update_query)
        self.conn.commit()
        print("Product updated successfully")



    def get_product_id(self, region, product, total, date, bo):
        self.cursor.execute(f"SELECT * FROM product WHERE region = {region} AND product = {product} AND total ={total} AND date = {date} AND bo = {bo}",)
        result = self.cursor.fetchone()
        print(result)
        if result:
            return result[0]
        else:
            return None
        

    def delete_product(self, id):
        delete_query = "DELETE FROM product WHERE id = %s"
        values = (id,)
        self.cursor.execute(delete_query, values)
        self.conn.commit()
        print("Product deleted successfully")

    def getAllProducts(self):
        select_all_query = "SELECT * FROM product"
        products = []
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        for row in rows:
            id, region, product, total, date, bo, up_to_date = row
            p = Product(id, region, product, total, date, up_to_date, bo)
            products.append(p)

        return products
    

    def create_update_trigger(mycursor):
        q="""CREATE if not exists TRIGGER update_product_trigger
    BEFORE UPDATE ON product
    FOR EACH ROW
    SET NEW.up_to_date = 'update';"""
        mycursor.execute(q)


