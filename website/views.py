from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import folium
import psycopg2

from website.databases.CRUD_bus import *
from website.databases.CRUD_driver import *
from website.databases.init_db import *
from website.databases.CRUD_bus_stop import *
from website.databases.CRUD_route_path import *
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

@views.route('/director_editor', methods=['GET', 'POST'])
def director_editor():
    return render_template("director_editor.html")

@views.route('/dispatcher_map', methods=['GET', 'POST'])
def dispatcher_map():
    return render_template("dispatcher_map.html")

@views.route('/add-bus', methods=['POST'])
def adding_bus():
    if request.method == 'POST':
        bus_number = request.form['bus_number']
        print(bus_number)
        add_bus(bus_number)
        return redirect(url_for('views.director_editor'))

@views.route('/add-driver', methods=['POST'])
def adding_driver():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        add_driver(full_name, email, password)

        return redirect(url_for('views.director_editor'))
    
@views.route('/add-route', methods=['POST'])
def adding_route():
    if request.method == 'POST':
        route_stops = request.form['bus_stop_name']
        route_stops = route_stops.split(' ')
        print(route_stops)

        return redirect(url_for('views.director_editor'))

@views.route('/add-bus-stop', methods=['POST'])
def adding_bus_stop():
    if request.method == 'POST':
        bus_stop_name = request.form['bus_stop_name']
        longitude = request.form['longitude']
        latitude = request.form['latitude']
        add_bus_stop(bus_stop_name, longitude, latitude)

        return redirect(url_for('views.director_editor'))

@views.route('/add-route-path', methods=['POST'])
def adding_route_path():
    if request.method == 'POST':
        route_id = request.form['id_route']
        list_coords = request.form['list_coords']
        add_route_path(route_id, list_coords)
        
        return redirect(url_for('views.director_editor'))