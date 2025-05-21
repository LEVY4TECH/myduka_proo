from flask import Flask,render_template,request,redirect,url_for,session,flash

from database import fetch_products,fetch_sales,insert_products,insert_sales,profit_per_product,profit_per_day,sales_per_product,sales_per_day,check_user,add_user

from flask_bcrypt import Bcrypt

from functools import wraps

app=Flask(__name__)
app.secret_key='levyyy'

bcrypt=Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected
    

@app.route('/products')
def products():
    products=fetch_products()
    return render_template('products.html',products=products)

@app.route('/add_products', methods=['POST'])
def add_products():
    
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
@login_required
def dashboard():
    profit_product=profit_per_product()
    sales_product=sales_per_product()
    profit_day=profit_per_day()
    sales_day=sales_per_day()

    product_name=[i[0] for i in profit_product]
    p_product=[ float(i[1]) for i in profit_product]
    s_product=[ float(i[1]) for i in sales_product]

    date=[ str(i[0]) for i in profit_day]
    p_day=[ float(i[1]) for i in profit_day]
    s_day=[ float(i[1]) for i in sales_day]
    
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
            flash("Please register to be a user", "error")
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(user[-1],password):
                session['email'] = email
                flash("Logged in successfully", "success")
                return redirect(url_for('home'))
            else:
                flash("Wrong password, Try again", "error")
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))




app.run(debug=True)