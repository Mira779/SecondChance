from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from voucher.extensions import db
from voucher.routes import voucher_bp
from models import Product, Purchase, Sale, Voucher, Size, VoucherItem

app = Flask(__name__)

# Stable Database path(saves database.db in the same folder as app.py)
# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:$bkmira4564M$@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(voucher_bp, url_prefix='/voucher')
    
def generate_item_code(product_id):
    return f"KD{product_id:03d}"

# Home Page
@app.route("/")
def index():
    return render_template('index.html')

# Add Product   
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    error = None

    if request.method == 'POST':
        name = request.form['name'].strip()
        category = request.form['category'].strip()
        
        try:
            buy_price = float(request.form['buy_price'])
            sell_price = float(request.form['sell_price'])
            quantity = int(request.form['quantity'])
            low_stock_limit = int(request.form['low_stock_limit'])
        except ValueError:
            error = "Please enter valid numbers."
            return render_template('add_product.html', error=error)
        
        new_product = Product(
            name = name,
            category = category,
            buy_price = buy_price,
            sell_price = sell_price,
            quantity = quantity,
            low_stock_limit = low_stock_limit
        )

        # First save to get ID
        db.session.add(new_product)
        db.session.commit()

        # Generate automatic item code using ID
        new_product.item_code = generate_item_code(new_product.id)
        db.session.commit()

        return redirect(url_for('show_products'))
    return render_template('add_product.html', error=error)

# View / Search products
@app.route('/products')
def show_products():
    search = request.args.get('search', '').strip()
    if search:
        products = Product.query.filter(
            (Product.item_code.contains(search)) |
            (Product.name.contains(search))
        ).all()
    else:
        products = Product.query.all()
    return render_template('products.html', products=products, search=search)

# Edit product
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    error = None
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        category = request.form['category'].strip()
        
        try:
            buy_price = float(request.form['buy_price'])
            sell_price = float(request.form['sell_price'])
            quantity = int(request.form['quantity'])
            low_stock_limit = int(request.form['low_stock_limit'])
        except ValueError:
            error = "Please enter valid numbers."
            return render_template('edit_product.html',product=product, error=error)
        
        product.name = name
        product.category = category
        product.buy_price = buy_price
        product.sell_price = sell_price
        product.quantity = quantity
        product.low_stock_limit = low_stock_limit

        db.session.commit()
        return redirect(url_for('show_products'))
    return render_template('edit_product.html', product=product, error=error)

# Delete product
@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('show_products'))

@app.route('/add_stock/<int:id>', methods=['GET', 'POST'])
def add_stock(id):
    product = Product.query.get_or_404(id)
    error = None
    
    if request.method == 'POST':
        try:
            qty = int(request.form['quantity'])
            price = float(request.form['buy_price'])
            if qty <= 0 or price <= 0:
                raise ValueError
        except:
            error = "Enter a valid values."
            return render_template('add_stock.html', product=product, error=error)
        
        product.quantity += qty
        purchase = Purchase(
            product_id=product.id,
            quantity=qty,
            buy_price=price
        )
        db.session.add(purchase)
        db.session.commit()
        return redirect(url_for('show_products'))
    return render_template('add_stock.html', product=product, error=error)

@app.route('/sell/<int:id>', methods=['GET', 'POST'])
def sell_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            quantity = request.form.get('quantity')
            buy_price = product.buy_price
            if not quantity or not quantity.isdigit():
                return "Invalid quantity"
            quantity = int(quantity)
            if quantity <= 0:
                return "Invalid quantity"
            
            if quantity > product.quantity:
                error = "Not enough stock."
                return error
            
            price = product.sell_price
            total = quantity * price
            profit = float(total - (quantity * float(buy_price)))
            today = datetime.now().strftime("%d-%m-%Y")
            # Count today's sales
            count = Sale.query.filter(Sale.voucher_no.like(f'V-{today}%')).count()+1
            voucher_no = f"v-{today}-{str(count).zfill(3)}"
            sale = Sale(
                voucher_no=voucher_no,
                product_id=product.id,
                product_name=product.name,
                item_code=product.item_code,
                quantity=quantity,
                price=price,
                total=total,
                profit=profit
            )
            db.session.add(sale)
            product.quantity -= quantity
            db.session.commit()

            # Show Voucher
            return render_template('sale_result.html', sale=sale)
        except Exception as e:
            return str(e)
    return render_template('sell_product.html', product=product)

@app.route('/dashboard')
def dashboard():
    products = Product.query.all()
    total_products = len(products)
    total_stock_value = sum(p.buy_price * p.quantity for p in products)
    low_stock = sum(1 for p in products if p.quantity <= p.low_stock_limit)
    total_profit = sum((p.sell_price - p.buy_price) * p.quantity for p in products)
    return render_template(
        'dashboard.html',
         total_products=total_products,
         total_stock_value=total_stock_value,
         low_stock=low_stock,
         total_profit=total_profit
    )

@app.route('/purchases')
def purchases():
    data = Purchase.query.order_by(Purchase.date.desc()).all()
    return render_template('purchases.html', data=data)

@app.route('/sales')
def sales():
    sales = Sale.query.all()
    return render_template('sales.html', sales=sales)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database + tables if not exist
    app.run(debug=True)
    