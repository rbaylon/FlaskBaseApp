from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
Bootstrap(app)

from baseapp import views
