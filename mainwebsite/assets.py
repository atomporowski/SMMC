import os
import re
import platform, webbrowser
from multiprocessing import Process
from os import path
from flask import Blueprint, render_template, flash, request, redirect
from flask_login import login_required, current_user
from .monitoring.ip_scanner import ip_scanner, device_list
from .datamodels import *
from . import save_data
import subprocess as sp

assets = Blueprint('assets', __name__)

current_os = platform.system()
save_path = 'mainwebsite/monitoring/'
file_name = 'servers_to_monitor'
regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


def read_servers():
    servers = Monitoring.query.filter_by(user_id=current_user.id).all()
    return servers


def servers_list():
    servers = read_servers()
    all_ip = []
    for server in servers:
        all_ip.append(server.server_ip)
    return all_ip


@assets.route('/assets')
@login_required
def default():
    return render_template("assets.html", user=current_user, device_list=device_list, servers=read_servers())


@assets.route('/scan', methods=['GET', 'POST'])
@login_required
def assets_list():
    target = Config.query.filter_by(user_id=current_user.id).first()
    if not target:
        flash("You should enter your network configuration in CONFIGURATION TAB before running Scan!",
              category='error')
        return default()
    # We have to remove the last IP octet as it will be changing within IP scanner
    target_ip = ".".join(target.network_ip.split('.')[0:-1]) + '.'
    p = Process(target=ip_scanner(target_ip))
    p.start()
    p.join()

    all_ip = servers_list()

    # Checking if the device was already scanned
    for device in device_list:
        if device not in all_ip:
            new_server = Monitoring(user_id=current_user.id, server_ip=device)
            db.session.add(new_server)
    db.session.commit()
    return default()


@assets.route('/assets/delete/<int:id>')
@login_required
def delete(id):
    server_to_delete = Monitoring.query.get_or_404(id)

    try:
        db.session.delete(server_to_delete)
        db.session.commit()
        flash('Server deleted successfully', category='success')
        return redirect('/assets')
    except:
        flash('There was a problem while deleting server')
        return render_template('assets.html', user=current_user, device_list=device_list, servers=read_servers())


@assets.route('/assets/addserver', methods=['GET', 'POST'])
@login_required
def add_server():
    if request.method == 'POST':
        user_id = current_user.id
        single_server = request.form.get('single_server')
        if re.search(regex, str(single_server)):
            new_server = Monitoring(user_id=user_id, server_ip=single_server)
            db.session.add(new_server)
            db.session.commit()
        else:
            flash('IP address is not valid.', category='error')
    return redirect('/assets')


@assets.route('/assets/makeserversfile')
@login_required
def make_file():
    all_ip = servers_list()
    save_data.save_data_to_file(all_ip, save_path, file_name)
    save_data.create_win_ini(all_ip, save_path, file_name='win_hosts')
    if path.exists(save_path + file_name + '.txt'):
        flash("Your file has been updated!", category="success")
    else:
        flash("Your file has been updated!", category="success")
    return redirect('/assets')


@assets.route('/assets/openconfigfile')
@login_required
def open_config_file():
    program_name = 'notepad.exe'
    directory = save_path + file_name + '.txt'
    if path.exists(directory):
        if current_os == 'Windows':
            sp.Popen([program_name, directory])
        elif current_os == 'Darwin':
            sp.call(['open', '-a', 'TextEdit', directory])
        else:
            webbrowser.open(directory)
    else:
        flash("You have no config file!", category='error')
    return redirect('/assets')


@assets.route('/assets/deleteconfigfile')
@login_required
def delete_config_file():
    if os.path.exists(save_path + file_name + '.txt'):
        os.remove(save_path + file_name + '.txt')
        flash('File removed successfully!', category='success')
    else:
        flash('There is no file to delete!', category='error')
    return redirect('/assets')
