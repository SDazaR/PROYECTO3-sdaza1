from flask import jsonify, Blueprint, render_template
from models.parlor import Parlor
from models.ingredient import Ingredient
from db.db import db

parlor_blueprint = Blueprint('parlor_bp', __name__, url_prefix="/parlor")

@parlor_blueprint.route("/<int:id>")
def index(id:int):
    parlor = Parlor.query.get(id)
    return render_template("index.html", menu=parlor.products, parlor_name=parlor.name, iden=id)

@parlor_blueprint.route("/<int:id>/bestProduct")
def best_product_handler(id:int):
    try:
        parlor = Parlor.query.get(id)
    except:
        return "No existe una heladería con ese id"
    resp = parlor.best_product()
    return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)

@parlor_blueprint.route("/<int:id>/makeSale/<product>")
def make_sale_handler(product:str, id:int):
    try:
        parlor = Parlor.query.get(id)
        if not parlor:
            return "No existe una heladería con ese id"
    except:
        resp = "No existe una heladería con ese id"
        return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)
    try:
        response = parlor.make_sale(product)  
    except ValueError as e:
        resp = str(e)
        return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)
    try:
        for ingredient in parlor.ingredients.copy():
            db_ingredient = Ingredient.query.get(ingredient.id)
            db.session.delete(db_ingredient)
            db.session.add(ingredient)
        db.session.commit()
    except Exception as e:
        resp =  "No se pudo actualizar los valores de la heladería. Causa:" + str(e)
        return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)

    resp = response

    return render_template("index.html", resp=resp, menu=parlor.products, parlor_name=parlor.name, iden=id)

