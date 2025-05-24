import psycopg2

conn=psycopg2.connect(user='postgres',password='leshan1234',host='localhost',port='5432',database='myduka_proo')

cur=conn.cursor()

def fetch_products():
    cur.execute('select * from products;')
    products=cur.fetchall()
    return products

def fetch_sales():
    cur.execute('select * from sales;')
    sales=cur.fetchall()
    return sales

def insert_products(values):
    insert="insert into products(productname,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_sales(values):
    insert="insert into sales(productid,quantity,created_at)values(%s,%s,now())"
    cur.execute(insert,values)
    conn.commit()

def profit_per_product():
    cur.execute("select products.productname, sum((products.selling_price-products.buying_price)*sales.quantity) as profit from products join sales on products.productid=sales.productid group by (products.productname);")
    profit_per_product=cur.fetchall()
    return profit_per_product

profit_product=profit_per_product()
# print(profit_product)

def profit_per_day():
    cur.execute("select date(sales.created_at), sum((products.selling_price-products.buying_price)*sales.quantity) as profit from products join sales on products.productid=sales.productid group by (sales.created_at);")
    profit_per_day=cur.fetchall()
    return profit_per_day

profit_day=profit_per_day()
# print(profit_day)

def sales_per_product():
    cur.execute("select products.productname, sum(products.selling_price*sales.quantity) as total_sales from products join sales on products.productid=sales.productid group by (products.productname);")
    sales_per_product=cur.fetchall()
    return sales_per_product

sales_product=sales_per_product()
# print(sales_product)

def sales_per_day():
    cur.execute("select date(sales.created_at), sum(products.selling_price*sales.quantity) as total_sales from products join sales on products.productid=sales.productid group by (sales.created_at);")
    sales_per_day=cur.fetchall()
    return sales_per_day

sales_day=sales_per_day()
# print(sales_day)


def check_user(email):
    query="select * from users where email = %s"
    cur.execute(query,(email,))
    user=cur.fetchone()
    return user

def add_user(values):
    insert="insert into users(firstname, lastname, email, password)values(%s, %s, %s, %s)"
    cur.execute(insert,values)
    conn.commit()

def total_sales():
    cur.execute("select sum(products.selling_price*sales.quantity) as total_sales from sales join products on sales.productid = products.productid")
    total_sales=cur.fetchall()
    return total_sales

x = total_sales()
# print(x)

def total_profit():
    cur.execute("select sum((products.selling_price - products.buying_price)*sales.quantity) as total_profit from products join sales on products.productid = sales.productid")
    total_profit = cur.fetchall()
    return total_profit

y = total_profit()
# print(y)

def total_sales_m():
    cur.execute("select sum(products.selling_price*sales.quantity) as total_sales_m from sales join products on sales.productid = products.productid WHERE DATE_TRUNC('month',sales.created_at::timestamp) = DATE_TRUNC('month',CURRENT_DATE);")
    total_sales_m = cur.fetchall()
    return total_sales_m

z = total_sales_m()
# print(z)

def total_profit_m():
    cur.execute("select sum((products.selling_price - products.buying_price)*sales.quantity) as total_profit_m from products join sales on products.productid = sales.productid WHERE DATE_TRUNC('month',sales.created_at::timestamp) = DATE_TRUNC('month',CURRENT_DATE);")
    total_profit_m = cur.fetchall()
    return total_profit_m

k = total_profit_m()
# print(k)
