from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html", user=current_user)


# @configuration.route('/configuration', methods=['GET', 'POST'])
# def network_configuration():
#     # curr = User.id
#     # print(curr)
#     test()
#     return render_template("configuration.html", user=current_user)
