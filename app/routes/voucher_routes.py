from flask import Blueprint, render_template, request, redirect, url_for
from app.models.voucher_table import Voucher, VoucherItem
from app.routes.extensions import db
from decimal import Decimal, InvalidOperation

voucher_bp = Blueprint('voucher', __name__)

#def generate_voucher_code(code):
    #code = int(code) #force int
    #return code

# Create and input weight to make an invoice
@voucher_bp.route('/vouchers', methods = ['GET', 'POST'])
def create_voucher():
    sizes_prices = [
        {'size': 'B' ,    'price': 4370},
        {'size': '28',    'price': 4370},
        {'size': '26',    'price': 4370},
        {'size': '24',    'price': 2720},
        {'size': '22',    'price': 2570},
        {'size': '20',    'price': 2150},
        {'size': '18',    'price': 1470},
        {'size': '16',    'price': 1400},
        {'size': '14',    'price': 1080},
        {'size': '12',    'price':  780},
        {'size': '10',    'price':  580},
        {'size': '8' ,    'price':   60},
        {'size': 'Repay', 'price':  165},
        {'size': 'Waste', 'price':    0}
    ]
    voucher = None # Must exist in all cases

    if request.method == 'POST':
        name = request.form.get('name')
        #1. Create voucher first
        voucher = Voucher(name=name)
        db.session.add(voucher)
        db.session.flush() # get voucher Id without full commit
        #print(voucher.id)
        total = Decimal('0.0')

        #2. Save items safely
        for item in sizes_prices:
            size = item['size']
            price = Decimal(str(item['price']))  # always decimal
            weight_input = request.form.get(f'weight_{size}')
            weight = Decimal('0.0')
            item_total = Decimal('0.0') # define item_total
            
            if weight_input:
                try:
                    weight = Decimal(weight_input)
                    item_total = (weight*Decimal(1.62)) * price
                except ValueError:
                    weight = Decimal('0.0')
            else:
                weight = 0.0

            total += item_total
                   
            new_item = VoucherItem(
                voucher_id=voucher.id,
                size=size,
                weight=float(weight), # store as float if DB expects it 
                price=price,
                total=item_total,
                grand_total=total
            )
            db.session.add(new_item)

        # 3. Update voucher total
        voucher.total = total
        print('final total: ', total)
        db.session.commit()

        return redirect(url_for('voucher.invoice', voucher_id=voucher.id))

    return render_template('Vouchers/voucher_table.html', sizes_prices=sizes_prices, voucher=voucher)

# Show printale invoice 
@voucher_bp.route('/invoice/<int:voucher_id>')
def invoice(voucher_id):
    voucher = Voucher.query.get_or_404(voucher_id)
    items = VoucherItem.query.filter_by(voucher_id=voucher_id).all()
    return render_template('Vouchers/invoice.html', voucher=voucher, items=items)

# Show invoice History
@voucher_bp.route('/voucher-history')
def voucher_history():
    vouchers = Voucher.query.order_by(Voucher.id.desc()).all()
    return render_template('Vouchers/history.html', vouchers=vouchers)

