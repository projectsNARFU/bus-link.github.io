from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import folium
import psycopg2

from website.databases.CRUD_bus import *
from website.databases.CRUD_driver import *
from website.databases.init_db import *
from website.databases.CRUD_bus_stop import *
# from . import db
import json

"""
файл с основными путями страниц
"""

def get_db_connection():
    conn = psycopg2.connect(
            host='localhost',
            dbname='postgres',
            user='postgres',
            password='qwer',
            port='5432')
    return conn


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
# @login_required
def supervisor():
    print(123)
    return render_template("authorization.html")