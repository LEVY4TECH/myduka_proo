from flask import Flask,render_template,request,redirect,url_for

from database import fetch_products,fetch_sales,insert_products,insert_sales,profit_per_product,profit_per_day,sales_per_product,sales_per_day,check_user,add_user

from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.secret_key='levyyy'

bcrypt=Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    products=fetch_products()
    return render_template('products.html',products=products)

@app.route('/add_products', methods=['GET','POST'])
def add_products():
    if request.method=='POST':
        productname=request.form['p_name']
        buying_price=request.form['b_price']
        selling_price=request.form['s_price']
        stock_quantity=request.form['s_quantity']
        new_product=(productname,buying_price,selling_price,stock_quantity)
        insert_products(new_product)
        return redirect(url_for('products'))


@app.route('/sales')
def sales():
    sales=fetch_sales()
    products=fetch_products()
    return render_template('/sales.html',sales=sales,products=products)

@app.route('/make_sales', methods=['GET','POST'])
def make_sales():
    if request.method=='POST':
        productid=request.form['pid']
        quantity=request.form['quantity']
        new_sale=(productid,quantity)
        insert_sales(new_sale)
        return redirect(url_for('sales'))

@app.route('/dashboard')
def dashboard():
    profit_product=profit_per_product()
    sales_product=sales_per_product()
    profit_day=profit_per_day()
    sales_day=sales_per_day()

    product_name=[i[0] for i in profit_product]
    p_product=[i[1] for i in profit_product]
    s_product=[i[1] for i in sales_product]

    date=[i[0] for i in profit_day]
    p_day=[i[1] for i in profit_day]
    s_day=[i[1] for i in sales_day]
    
    return render_template('dashboard.html',product_name=product_name,p_product=p_product,s_product=s_product,date=date,p_day=p_day,s_day=s_day)

@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        firstname=request.form['fname']
        lastname=request.form['lname']
        email=request.form['email']
        password=request.form['pass']

        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        user=check_user(email)

        if not user:
            new_user=(firstname,lastname,email,hashed_password)
            add_user(new_user)
            return redirect(url_for('login'))
        else:
            print('Already Registered')
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['pass']

        user=check_user(email)

        if not user:
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(user[-1],password):
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html')



app.run(debug=True)