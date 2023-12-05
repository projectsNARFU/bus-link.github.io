from flask import Blueprint, render_template, render_template_string, request, flash, jsonify
from flask_login import login_required, current_user
import folium
from folium import PolyLine
from folium.plugins import Draw
from flask import Flask
from geopy.distance import geodesic
import math
import random

"""
файл с основными путями страниц
"""


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# @login_required
def supervisor():
    return render_template("supervisor.html", user=current_user)




@views.route('/traffic-controller', methods=['GET', 'POST'])
def traffic_controller():
    global mapObj, Bus, markers
    mapObj = folium.Map(location=[64.53827, 40.4245],
                        zoom_start=14, width=800, height=500)

    # add a marker to the map object
    folium.Marker([17.4127332, 78.078362],
                  popup="<i>This a marker</i>").add_to(mapObj)

    # Добавляем несколько маркеров
    markers = [(64.54161, 40.39945), (64.53747, 40.41655), (64.53537, 40.43097), (64.53382, 40.44243), (64.53206, 40.45398), (64.53209, 40.46036), (64.53297, 40.4708)]
    start_coordinates = markers[0]
    for marker in markers:
        folium.Marker(location=marker).add_to(mapObj)

    # Создаем отдельный маркер с изображением
    icon_url = 'BSicon_BUS.svg.png'
    icon = folium.features.CustomIcon(icon_url, icon_size=(40, 40))
    Bus = folium.Marker(location=start_coordinates, icon=icon, draggable=True)
    Bus.add_to(mapObj)


    # DTP = folium.Marker(location=(64.5340251352963, 40.43985944959183), draggable=True)
    # DTP.add_to(mapObj)


    # Добавляем линию PolyLine на карту
    line_points = [[64.54158, 40.39934], [64.54074, 40.40095], [64.54051, 40.40125], [64.54001, 40.40232], [64.53947, 40.40394],
                   [64.53898, 40.40585], [64.53865, 40.40765], [64.53857, 40.4082], [64.53755, 40.41549], [64.53737, 40.41662],
                   [64.53404, 40.43952], [64.53387, 40.44188], [64.53358, 40.44394], [64.53331, 40.44548], [64.53302, 40.44681],
                   [64.53221, 40.45156], [64.53198, 40.45446], [64.53202, 40.45622], [64.53203, 40.45775], [64.53208, 40.46304],
                   [64.53243, 40.4642], [64.53291, 40.47069]]

    polyline = PolyLine(locations=line_points, color='blue')
    polyline.add_to(mapObj)

    #Даёт возможность ставить метки на карте
    draw = Draw()
    draw.add_to(mapObj)

    # Генерируем случайные числа для каждой точки
    max_value = 25  # Максимальное значение
    values = [random.randint(0, max_value) for _ in range(len(markers))]

    # Определяем цвета в зависимости от значений
    color_scale = ['green', 'yellow', 'red']
    colors = [color_scale[math.floor(value / (max_value / len(color_scale)))] for value in values]

    # Определяем масштаб для радиуса круга
    max_radius = 25  # Максимальный радиус круга
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

    return render_template('traffic_controller.html', user=current_user,
                           header=header, body_html=body_html, script=script)


# Обновление координат маркера на карту
@views.route('/update_marker', methods=['POST'])
def update_marker():
    global current_marker_index

    if current_marker_index < len(markers):
        # Получаем следующую координату из списка
        next_coordinates = markers[current_marker_index]
        current_marker_index += 1  # Увеличиваем индекс для следующего раза

        # Возвращаем текущую координату для обновления маркера на карте
        return jsonify({'lat': next_coordinates[0], 'lng': next_coordinates[1]})
    else:
        # Когда все координаты использованы, возвращаем пустой JSON
        return jsonify({})







#без html(пока убрал)
# #Эта функция должна обновлять местоположения автобуса на карте
# @views.route('/update_marker', methods=['POST'])
# def update_marker():
#     global current_marker_index, mapObj, Bus, markers
#     if 'current_marker_index' not in globals():
#         current_marker_index = 0
#
#     if current_marker_index < len(markers):
#         new_coords = markers[current_marker_index]
#         Bus.location = new_coords
#         mapObj.get_root().render()
#
#         current_marker_index += 1
#     else:
#         current_marker_index = 0
#         new_coords = markers[current_marker_index]
#         Bus.location = new_coords
#         mapObj.get_root().render()
#
#     return '', 204

#Должна создовать маркеры по кнопе и записывать  их координаты
@views.route('/add_marker', methods=['POST'])
def add_marker():
    lat = request.form['lat']  # получаем широту из запроса
    lon = request.form['lon']  # получаем долготу из запроса

    with open('marker_coords.txt', 'a') as file:  # открываем файл для добавления координат
        file.write(f"Marker coordinates: {lat}, {lon}\n")  # записываем координаты в файл

    return '', 204  # возвращаем пустой ответ с кодом статуса 204 (No Content)

@views.route('/traffic-controller', methods=['GET', 'POST'])

@views.route('/traffic-controller/chat', methods=['GET', 'POST'])
def traffic_controller_chat():
    test_list_drivers = ['vanya', 'dima', 'bob']
    return render_template("traffic_controller_chat.html", user=current_user, drivers=test_list_drivers)

#Расчитывает расстояние между точками(пока их нужно задавать вручную)
def calculate_and_save_distance(coord1, coord2, output_file):
    # Рассчитываем расстояние с помощью библиотеки geopy
    distance = geodesic(coord1, coord2).kilometers

    # Записываем расстояние в текстовый файл
    with open(output_file, 'w') as file:
        file.write(f'Расстояние между точками: {distance} км\n')

    print(f"Расстояние успешно рассчитано и сохранено в файл {output_file}")

# Пример использования функции
coord1 = (64.54161, 40.39945)  # Координаты первой точки
coord2 = (64.53747, 40.41655)  # Координаты второй точки
output_file = "marker_coords.txt"
calculate_and_save_distance(coord1, coord2, output_file)

#штмд код убрал
# #При нажатии правой кнопки мыши должна появиться менющка в которой предложат создать маркер и его координаты запишуться в txt
# @views.route('/')
# def index():
#     return render_template('traffic_controller.html')  # Предположим, что ваш шаблон называется index.html
# #продолжегие прошлой функции
# @views.route('/save-coordinates', methods=['POST'])
# def save_coordinates():
#     lat = request.form.get('lat')
#     lng = request.form.get('lng')
#
#     # Записываем координаты маркера в текстовый файл
#     with open('coordinates.txt', 'a') as file:
#         file.write(f'{lat},{lng}\n')
#
#     return 'success'


@views.route('/driver', methods=['GET', 'POST'])
def driver():
    return render_template("driver.html", user=current_user)


@views.route('/passenger', methods=['GET', 'POST'])
def passenger():
    return render_template("passenger.html", user=current_user)


