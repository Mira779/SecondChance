class TableService:

    @staticmethod
    def model_to_row(model, meta):

        row = {}

        for column in meta["columns"]:

            field = column["field"]

            row[field] = getattr(model, field)

        row["id"] = model.id

        return row
    