from flask import Blueprint, render_template, request, redirect, url_for
from app.models.raw_table import Raw
from app.routes.extensions import db
from sqlalchemy import text

raw_bp = Blueprint('raw', __name__)

def generate_item_code(Kd, bag_no):
        Item_code = f"KD-{Kd}//{bag_no}"
        return Item_code

@raw_bp.route('/raws', methods = ['GET', 'POST'])
def raws():
    error = None
    allowed_names = ['SPN-3', 'HSW', 'NSY', 'AKS', 'Counter', 'PYI', 'KPT']
    
    if request.method == 'POST':
        try:
            kd = int(request.form['kd'])
            bag_no = int(request.form['bag_no'])
            # Validation Rule
            if bag_no > kd:
                raise ValueError("Invalid")

            weight = float(request.form['weight'])
            price = int(request.form['price'])
        except ValueError:
            error = "Enter valid numbers."
            return render_template('product/raw.html', error=error)

        name = request.form.get('name')
        if name not in allowed_names:
            return "Invalid name"

        new_raw_product = Raw(
            kd=kd,
            bag_no=bag_no,
            weight = weight,
            price = price,
            name = name
        )
        try:
            # First save to get ID
            db.session.add(new_raw_product)
            db.session.commit()
            #result = db.session.execute(text("SELECT * FROM raws"))
            #return str(list(result))

        except Exception as e:
            db.session.rollback()
            print('error:', e)

        # Generate automatic item code 
        new_raw_product.item_code = str(generate_item_code(kd, bag_no))
        db.session.commit()
        return redirect(url_for('raw.show_products'))
    return render_template('product/raw.html', allowed_names=allowed_names)

@raw_bp.route('/products')
def show_products():
    products = Raw.query.all()
    return render_template('product/raw_table.html', products=products)

# View / Search products
@raw_bp.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return redirect('/products')
    results = Raw.query.filter(
        (Raw.kd == int(query) if query.isdigit() else False) |
        (Raw.name.contains(query))
    ).all()
    
    return render_template('product/search.html', raws=results, query=query)

# Delete product
@raw_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Raw.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('raw.show_products'))

'''
# Edit product
@raw_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Raw.query.get_or_404(id)
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
'''

# Start here
