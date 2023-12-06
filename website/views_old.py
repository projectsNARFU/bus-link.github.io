from flask import Blueprint, render_template, render_template_string, request, flash, jsonify
from flask_login import login_required, current_user
import folium
import psycopg2
# from . import db
import json
from website.databases.CRUD_bus import *
from website.databases.CRUD_driver import *
from website.databases.init_db import *
from website.databases.CRUD_bus_stop import *


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


views_old = Blueprint('views_old', __name__)


@views_old.route('/', methods=['GET', 'POST'])
# @login_required
def supervisor():
    return render_template("supervisor.html", user=current_user)


@views_old.route('/traffic-controller', methods=['GET', 'POST'])
def traffic_controller():

    mapObj = folium.Map(location=[18.906286495910905, 79.40917968750001],
                        zoom_start=5, width=800, height=500)

    # add a marker to the map object
    folium.Marker([17.4127332, 78.078362],
                popup="<i>This a marker</i>").add_to(mapObj)

    # render the map object
    mapObj.get_root().render()

    # derive the script and style tags to be rendered in HTML head
    header = mapObj.get_root().header.render()

    # derive the div container to be rendered in the HTML body
    body_html = mapObj.get_root().html.render()

    # derive the JavaScript to be rendered in the HTML body
    script = mapObj.get_root().script.render()

    # print(header, body_html, script)

    return render_template('traffic_controller.html', user=current_user, 
                        header=header, body_html=body_html, script=script)
                        


@views_old.route('/traffic-controller/chat', methods=['GET', 'POST'])
def traffic_controller_chat():
    # test_list_drivers = ['vanya', 'dima', 'bob']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM drivers;')
    drivers = cur.fetchall()
    cur.close()
    conn.close()
    print(drivers)

    return render_template("traffic_controller_chat.html", user=current_user, drivers=drivers)


@views_old.route('/driver', methods=['GET', 'POST'])
def driver():
    return render_template("driver.html", user=current_user)


@views_old.route('/passenger', methods=['GET', 'POST'])
def passenger():
    return render_template("passenger.html", user=current_user)

@views_old.route('/input_test', methods=['GET', 'POST'])
def test():
    # add_driver('qwe wer wer', 'qweasd@mail.ru', 'qwerty')
    # add_driver('qwe wer wer2', 'bgfd@mail.ru', 'asdf')
    # add_driver('qwe wer wer3', 'nfgdd@mail.ru', 'zxcv')
    drivers = Driver.select().order_by(Driver.id_driver)
    drivers = drivers.dicts().execute()[:]
    print(drivers)
    return render_template("input_test.html", drivers=drivers)

# ADD BUS STOP
@views_old.route('/addstop', methods=["POST"])
def adding_bus_stop():
    if request.method == 'POST':
        bus_stop_name = request.form['bus_stop_name']
        longitude = request.form['longitude']
        latitude = request.form['latitude']
        add_bus_stop(bus_stop_name, longitude, latitude)

        return redirect(url_for('views.traffic_controller'))
    
# ADD BUS
@views_old.route('/addbus', methods=["POST"])
def adding_bus():
    if request.method == 'POST':
        bus_number = request.form['bus_number']
        add_bus(bus_number)

        return redirect(url_for('views.traffic_controller'))

# ADD DRIVER
@views_old.route('/adddriver', methods=["POST"])
def adding_driver():
    if request.method == 'POST':
        driver_name = request.form['driver_name']
        driver_email = request.form['driver_email']
        driver_pass = request.form['driver_pass']
        add_driver(driver_name, driver_email, driver_pass)

        return redirect(url_for('views.traffic_controller'))