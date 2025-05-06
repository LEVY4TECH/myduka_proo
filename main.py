from flask import Flask,render_template,request,redirect,url_for

from database import fetch_products,fetch_sales,insert_products,insert_sales

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    products=fetch_products()
    return render_template('products.html',products=products)

@app.route('/sales')
def sales():
    sales=fetch_sales()
    return render_template('/sales.html',sales=sales)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/base')
def base():
    return render_template('base.html')

app.run(debug=True)