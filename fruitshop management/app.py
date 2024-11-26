from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # your MySQL username
app.config['MYSQL_PASSWORD'] = 'tamil_2005'  # your MySQL password
app.config['MYSQL_DB'] = 'Fruitshop_db'  # your MySQL database name
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')  # Home page with buttons

@app.route('/products')
def products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('landing.html', products=products)

@app.route('/add_product_form')
def add_product_form():
    return render_template('add_product.html')  # A form to add new products
@app.route('/add_product', methods=['POST'])
def add_product():
    product_id = request.form['product_id']  # Assuming you're getting the product ID from the form
    conn = mysql.connect()
    cur = conn.cursor()

    # Use the correct column name 'ItemNo' instead of 'id'
    cur.execute("SELECT * FROM products WHERE ItemNo = %s", (product_id,))
    product = cur.fetchone()

    if product:
        return "Product already exists!"
    
    # Insert new product logic here
    product_name = request.form['product_name']
    kg = request.form['kg']
    price = request.form['price']
    
    cur.execute(
        "INSERT INTO products (ItemNo, FruitName, Kg, Price) VALUES (%s, %s, %s, %s)",
        (product_id, product_name, kg, price)
    )
    conn.commit()
    conn.close()

    return redirect('/products')



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cur.fetchone()
    cur.close()
    
    if request.method == 'POST':
        name = request.form['name']
        kg = request.form['kg']
        price = request.form['price']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE products SET name = %s, kg = %s, price = %s WHERE id = %s",
                    (name, kg, price, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/products')
    
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:id>')
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/products')

if __name__ == "__main__":
    app.run(debug=True)
