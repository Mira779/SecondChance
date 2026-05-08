from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from app.models.raw_table import Raw

from app.metadata.product_meta import product_meta

from app.services.crud_service import CrudService
from app.services.table_service import TableService

from app.routes.extensions import db


product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/product"
)


# ====================================
# PRODUCT LIST
# ====================================

@product_bp.route("/list")
def product_list():

    products = Raw.query.all()

    rows = []

    for product in products:

        row = TableService.model_to_row(
            product,
            product_meta
        )

        rows.append(row)

    return render_template(
        "components/list.html",
        meta=product_meta,
        rows=rows
    )


# ====================================
# ADD PRODUCT
# ====================================

@product_bp.route("/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product = Raw()

        CrudService.save_model(
            product,
            product_meta,
            request.form
        )

        return redirect(
            url_for("product.product_list")
        )

    return render_template(
        "components/add.html",
        meta=product_meta
    )


# ====================================
# EDIT PRODUCT
# ====================================

@product_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    product = Raw.query.get_or_404(id)

    if request.method == "POST":

        CrudService.update_model(
            product,
            product_meta,
            request.form
        )

        return redirect(
            url_for("product.product_list")
        )

    return render_template(
        "components/add.html",
        meta=product_meta,
        item=product
    )


# ====================================
# DELETE PRODUCT
# ====================================

@product_bp.route("/delete/<int:id>")
def delete_product(id):

    product = Raw.query.get_or_404(id)

    CrudService.delete_model(product)

    return redirect(
        url_for("product.product_list")
    )
