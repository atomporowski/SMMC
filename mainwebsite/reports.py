from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .datamodels import *

reports = Blueprint('reports', __name__)


def read_unique_devices():
    dashboard_data = []
    device_details = {}
    all_data = Clients_data.query.all()
    all_data.reverse()

    def check(dic_list, value):
        for elem in dic_list:
            if value in elem.values():
                return True
        return False

    for i in all_data:
        device_details = {
            'hostname': i.hostname,
            'os': i.os,
            'ip': i.server_ip,
            'boot_time': i.boot_time,
            'cpu_percent': i.cpu_percent,
            'memory_percent': i.memory_percent,
            'virtual_mem': i.virtual_mem,
            'avg_load': i.avg_load,
            'timestamp': i.timestamp
        }
        if check(dashboard_data, i.hostname):
            continue
        else:
            dashboard_data.append(device_details)
            continue

    return dashboard_data


@reports.route('/reports', methods=['GET', 'POST'])
@login_required
def network_reports():
    return render_template("reports.html", user=current_user, devices=read_unique_devices())
