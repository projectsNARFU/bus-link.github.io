from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import folium
import psycopg2
from datetime import datetime
from pathlib import Path 

from folium import PolyLine
from folium.plugins import Draw
from geopy.distance import geodesic
import math
import random

from website.databases.CRUD_bus import *
from website.databases.CRUD_driver import *
from website.databases.init_db import *
from website.databases.CRUD_bus_stop import *
from website.databases.CRUD_route_path import *
from .passengers import *
# from . import db
import json

"""
файл с основными путями страниц
"""

views = Blueprint('views', __name__)
click = False

@views.route('/', methods=['GET', 'POST'])
# @login_required
def authorization():
    return render_template("test_auth.html")

@views.route('/director_map', methods=['GET', 'POST'])
def director_map():
    global mapObj, Bus, markers, mark, click, current_time, speed_bus, i, x, koordinate_x, koordinate_y
    mapObj = folium.Map(location=[64.53827, 40.4245],
                        zoom_start=14, width=1500, height=750)

    # add a marker to the map object
    folium.Marker([17.4127332, 78.078362],
                  popup="<i>This a marker</i>").add_to(mapObj)
    
    # Добавляем линию PolyLine на карту
    line_points = [[64.54158, 40.39934], [64.54074, 40.40095], [64.54051, 40.40125], [64.54001, 40.40232], [64.53947, 40.40394],
                   [64.53898, 40.40585], [64.53865, 40.40765], [64.53857, 40.4082], [64.53755, 40.41549], [64.53737, 40.41662],
                   [64.53404, 40.43952], [64.53387, 40.44188], [64.53358, 40.44394], [64.53331, 40.44548], [64.53302, 40.44681],
                   [64.53221, 40.45156], [64.53198, 40.45446], [64.53202, 40.45622], [64.53203, 40.45775], [64.53208, 40.46304],
                   [64.53243, 40.4642], [64.53291, 40.47069]]
    # Добавляем несколько маркеров
    markers = [(64.54161, 40.39945), (64.53747, 40.41655), (64.53537, 40.43097), (64.53382, 40.44243), (64.53206, 40.45398), (64.53209, 40.46036), (64.53297, 40.4708)]
    start_coordinates = markers[0]
    for marker in markers:
        folium.Marker(location=marker).add_to(mapObj)

    # add_route_path(64.54051, 40.40125)

    # route_path = RoutePath.select().where(RoutePath.id_route_path == 1)
    # route_path = route_path.dicts().execute()[0]
    # print(route_path['coord_longitude'])
    # # print(float(route_path['coord_longitude']), float(route_path['coord_latitude']))
    # mark = (float(route_path['coord_longitude']), float(route_path['coord_latitude']))

    if click == False:
        i = 0
        x = 1
        koordinate_x = 64.54158
        koordinate_y = 40.39934
        mark = koordinate_x, koordinate_y
        now_2 = datetime.now()
        h = now_2.strftime('%H')
        m = now_2.strftime('%M')
        s = now_2.strftime('%S')
        current_time = int(s) + int(m) * 60 + int(h) * 3600
    else:
        speed_bus = 24.73 / 3600
        now_2 = datetime.now()
        h = now_2.strftime('%H')
        m = now_2.strftime('%M')
        s = now_2.strftime('%S')
        current_time2 = int(s) + int(m) * 60 + int(h) * 3600
        time = current_time2 - current_time
        road = [0.12, 0.03, 0.08, 0.10, 0.11, 0.09, 0.03, 0.37, 0.06, 1.16, 0.11,
                0.10, 0.08, 0.07, 0.25, 0.14, 0.08, 0.07, 0.25, 0.07, 0.32]
        if time/9 % 60 == 0:
            road = road[::-1]
        distanse = time * speed_bus
        s = 0
        d = 0
        f = 0
        for i in range(len(road) - 1):
            if distanse > s:
                s += road[i]
                f += 1
            else:
                d = s
        asa = d - distanse



        from geopy.distance import geodesic

        def calculate_bus_coordinates(start_point, end_point, distance):
            total_distance = geodesic(start_point, end_point).kilometers

            ratio = distance / total_distance
            x = start_point[0] + ratio * (end_point[0] - start_point[0])
            y = start_point[1] + ratio * (end_point[1] - start_point[1])

            return x, y

        mark = calculate_bus_coordinates(line_points[f - 1], line_points[f], asa)
        print(mark)

    # Создаем отдельный маркер с изображением
    # icon_url = "./BSicon_BUS.png"
    icon_url = str(Path("BSicon_BUS.png"))
    icon = folium.features.CustomIcon(icon_url, icon_size=(40, 40))
    Bus = folium.Marker(location=(mark), icon=icon,  draggable=True)
    Bus.add_to(mapObj)


    # DTP = folium.Marker(location=(64.5340251352963, 40.43985944959183), draggable=True)
    # DTP.add_to(mapObj)



    polyline = PolyLine(locations=line_points, color='blue')
    polyline.add_to(mapObj)

    #Даёт возможность ставить метки на карте
    draw = Draw(export=True)
    draw.add_to(mapObj)


    # Генерируем случайные числа для каждой точки
    values = list(passengers_on_stops(stops_dict).values())
    max_value=max(values)

    # # Предотвращение выхода за пределы
    # values = [max(0, min(value, max_value)) for value in values]

    # Определяем цвета в зависимости от значений
    color_scale = ['green', 'yellow', 'red']
    colors = [color_scale[math.floor(value / (26 / len(color_scale)))] for value in values]

    # Определяем масштаб для радиуса круга
    max_radius = 20  # Максимальный радиус круга
    min_radius = 5  # Минимальный радиус круга

    # Добавляем круги на карту
    for coord, value, color in zip(markers, values, colors):
        radius = (value / max_value) * (max_radius - min_radius) + min_radius
        folium.CircleMarker(
            location=coord,
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=f'Значение: {value}',
            tooltip=str(value)
        ).add_to(mapObj)


    # render the map object
    mapObj.get_root().render()

    # derive the script and style tags to be rendered in HTML head
    header = mapObj.get_root().header.render()

    # derive the div container to be rendered in the HTML body
    body_html = mapObj.get_root().html.render()

    # derive the JavaScript to be rendered in the HTML body
    script = mapObj.get_root().script.render()

    # print(header, body_html, script)
    print(Bus.location)
    return render_template("director_map.html", user=current_user,
                           header=header, body_html=body_html, script=script)

@views.route('/update_marker', methods=['POST'])
def update_marker():
    global click
    if request.method == 'POST':
        button_name = request.form['button']
        print(button_name)
        if button_name:
            print(1)
        click = True
    #     new_coord = request.form["new_coord"]
    #     mark = list((float(x) for x in new_coord.split(",")))
        print(Bus.location)
        return redirect(url_for("views.director_map"))

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