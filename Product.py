class Product:
    def __init__(self,id,region,product,total,date ,up_to_date, bo) :
        self.id=id
        self.region=region
        self.date=date
        self.total=total
        self.product=product
        self.up_to_date=up_to_date
        self.bo = bo


    def get_up_to_date(self):
        return self.up_to_date
    def get_id(self):
        return self.id
    def get_date(self):
        return self.date
    def set_up_to_date(self,up_to_date):
        self.up_to_date=up_to_date
    def set_date(self,date):
        self.date=date

    def __str__(self) -> str:
        return f'''
        {self.id}
        {self.region}
        {self.date}
        {self.total}
        {self.product}
        {self.up_to_date}
        
        '''