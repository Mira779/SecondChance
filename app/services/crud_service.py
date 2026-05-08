from app.routes.extensions import db


class CrudService:

    @staticmethod
    def save_model(model, meta, form_data):

        for field in meta["fields"]:

            field_name = field["name"]

            value = form_data.get(field_name)

            setattr(model, field_name, value)

        db.session.add(model)

        db.session.commit()

        return model

    @staticmethod
    def update_model(model, meta, form_data):

        for field in meta["fields"]:

            field_name = field["name"]

            value = form_data.get(field_name)

            setattr(model, field_name, value)

        db.session.commit()

        return model

    @staticmethod
    def delete_model(model):

        db.session.delete(model)

        db.session.commit()
