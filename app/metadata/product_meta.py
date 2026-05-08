product_meta = {

    "title": "Product Management",

    # =========================
    # FORM FIELDS
    # =========================

    "fields": [

        {
            "name": "bag_no",
            "label": "Bag No.",
            "type": "number",
            "required": True
        },

        {
            "name": "KD",
            "label": "KD(batch)",
            "type": "number",
            "required": True
        },

        {
            "name": "weight",
            "label": "Weight(Kg)",
            "type": "number",
            "required": True
        },

        {
            "name": "price",
            "label": "Price",
            "type": "number",
            "required": True
        },

        {
            "name": "allow_names",
            "label": "Choose the Branch",

            "type": "select",

            "class": "form-select",

            "choices": [
                'SPN-3',
                'HSW',
                'NSY',
                'AKS',
                'Counter',
                'PYI',
                'KPT'
            ]
        }
    ],

    # =========================
    # TABLE COLUMNS
    # =========================

    "columns": [

        {
            "field": "bag_no",
            "label": "Bag No."
        },

        {
            "field": "kd",
            "label": "KD"
        },

        {
            "field": "name",
            "label": "Product"
        },

        {
            "field": "price",
            "label": "Price",
            "type": "currency"
        },

        {
            "field": "created_at",
            "label": "Date"
        }
    ],

    # =========================
    # ACTION BUTTONS
    # =========================

    "actions": [

        {
            "label": "Edit",
            "endpoint": "product.edit_product",
            "class": "btn btn-warning btn-sm"
        },

        {
            "label": "Delete",
            "endpoint": "product.delete_product",
            "class": "btn btn-danger btn-sm"
        }
    ]
}
