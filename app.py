from flask import Flask, render_template
from controllers.parlor_controller import parlor_blueprint
import os
from urllib.parse import quote_plus
from db.db import db, init_db
from db.init_data import fill_db
from models.parlor import Parlor

app = Flask(__name__, template_folder="views")
app.register_blueprint(parlor_blueprint)
@app.route("/")
def index():
    parlors = Parlor.query.all()
    return render_template("welcome.html", parlors=parlors)

app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{os.getenv("DB_USER_NAME")}:{quote_plus(os.getenv("DB_PASSWORD"))}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app=app)

init_db(app)
fill_db(app, db)

if __name__ == '__main__':
    app.run(debug=True)