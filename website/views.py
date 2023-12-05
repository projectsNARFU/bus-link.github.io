from flask import Blueprint, render_template, render_template_string, request, flash, jsonify
from flask_login import login_required, current_user
import folium
import psycopg2
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
    return render_template("supervisor.html", user=current_user)


@views.route('/traffic-controller', methods=['GET', 'POST'])
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


@views.route('/traffic-controller/chat', methods=['GET', 'POST'])
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


@views.route('/driver', methods=['GET', 'POST'])
def driver():
    return render_template("driver.html", user=current_user)


@views.route('/passenger', methods=['GET', 'POST'])
def passenger():
    return render_template("passenger.html", user=current_user)