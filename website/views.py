from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json


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
    return render_template("traffic_controller.html", user=current_user)


@views.route('/traffic-controller/chat', methods=['GET', 'POST'])
def traffic_controller_chat():
    return render_template("traffic_controller_chat.html", user=current_user)


@views.route('/driver', methods=['GET', 'POST'])
def driver():
    return render_template("driver.html", user=current_user)


@views.route('/passenger', methods=['GET', 'POST'])
def passenger():
    return render_template("passenger.html", user=current_user)