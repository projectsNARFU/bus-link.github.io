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

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
# @login_required
def authorization():
    return render_template("test_auth.html")

@views.route('/director_map', methods=['GET', 'POST'])
def director_map():
    return render_template("director_map.html")

@views.route('/director_routes', methods=['GET', 'POST'])
def director_routes():
    return render_template("director_routes.html")

@views.route('/dispatcher_map', methods=['GET', 'POST'])
def dispatcher_map():
    return render_template("dispatcher_map.html")
