from flask import Blueprint, render_template, request, redirect, url_for
from app.models.voucher_table import Voucher, VoucherItem
from app.routes.extensions import db

voucher_bp = Blueprint('voucher', __name__)

#def generate_voucher_code(code):
    #code = int(code) #force int
    #return code
@voucher_bp.route('/vouchers', methods = ['GET', 'POST'])
def create_voucher():
    sizes_prices = [
        {'size': 'B' ,    'weight':'', 'price': 4370, 'total':''},
        {'size': '28',    'weight':'', 'price': 4370, 'total':''},
        {'size': '26',    'weight':'', 'price': 4370, 'total':''},
        {'size': '24',    'weight':'', 'price': 2720, 'total':''},
        {'size': '22',    'weight':'', 'price': 2570, 'total':''},
        {'size': '20',    'weight':'', 'price': 2150, 'total':''},
        {'size': '18',    'weight':'', 'price': 1470, 'total':''},
        {'size': '16',    'weight':'', 'price': 1400, 'total':''},
        {'size': '14',    'weight':'', 'price': 1080, 'total':''},
        {'size': '12',    'weight':'', 'price':  780, 'total':''},
        {'size': '10',    'weight':'', 'price':  580, 'total':''},
        {'size': '8' ,    'weight':'', 'price':   60, 'total':''},
        {'size': 'Repay', 'weight':'', 'price':  165, 'total':''},
        {'size': 'Waste', 'weight':'', 'price':    0, 'total':''}
    ]
    

    if request.method == 'POST':
        
        grand_total = 0.0
        total = 0.0
        # 2.Loop through predefined list
        for i in range(len(sizes_prices)):

            name = request.form.get('name')
            #1. Create voucher
            voucher = Voucher(name=name)
            db.session.add(voucher)
            db.session.commit() # get voucher Id
            print(voucher.id)

            size = request.form.get(f'size_{i}')
            price = float(request.form.get(f'price_{i}') or 0)
            weight = float(request.form.get(f'weight_{i}') or 0)
            if weight and price:
                total = weight * price
                grand_total += float(total)
            else:
                total = 0
        
        #if weight: # only save filled rows
        new_item = VoucherItem(
            voucher_id=voucher.id,
            size=size,
            weight=weight,
            price=price,
            total=total,
            grand_total=grand_total,
            name=name
        )

        db.session.add(new_item)
        # 3. Save to database
        db.session.commit()

        return redirect(url_for('voucher.invoice', voucher_id=voucher.id))

    return render_template('Vouchers/voucher_table.html', sizes_prices=sizes_prices, voucher=voucher)


@voucher_bp.route('/invoice/<int:voucher_id>')
def invoice(voucher_id):
    print("voucher: ", voucher)
    voucher = Voucher.query.get(voucher_id)
    items = VoucherItem.query.filter_by(voucher_id=voucher_id).all()
    return render_template('Vouchers/invoice.html', voucher=voucher, items=items)

