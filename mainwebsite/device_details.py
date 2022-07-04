import pygal

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .datamodels import *

device_details = Blueprint('device_details', __name__)


@device_details.route('/reports/<device>', methods=['GET', 'POST'])
@login_required
def details(device):
    monitoring_data = Clients_data.query.filter(Clients_data.hostname == device).all()

    return render_template("device_details.html", user=current_user, device=device,
                           cpu_usage=generate_chart(device, monitoring_data, resource='cpu_percent'),
                           memory_usage=generate_chart(device, monitoring_data, resource='memory_percent'),
                           virtual_mem_usage=generate_chart(device, monitoring_data, resource='virtual_mem'),
                           avg_load=generate_chart(device, monitoring_data, resource='avg_load'))


def generate_chart(device, monitoring_data, resource):
    graph = pygal.Line(x_label_rotation=45, width=1500, height=250, legend_box_size=4, value_font_size=1,
                       inner_radius=0.70)
    graph.title = device + ' ' + resource + ' ' + 'usage'
    graph.range = [0, 100]
    resource_usage_list = []
    timestamps_list = []
    print(monitoring_data)
    for entry in monitoring_data:
        if resource == 'memory_percent':
            resource_usage_list.append(entry.memory_percent)
        elif resource == 'cpu_percent':
            resource_usage_list.append(entry.cpu_percent)
        elif resource == 'virtual_mem':
            resource_usage_list.append(entry.virtual_mem)
        elif resource == 'avg_load':
            resource_usage_list.append(entry.avg_load)
        timestamps_list.append(entry.timestamp[11:16])
    graph.add("%", resource_usage_list[-60:])
    graph.x_labels = timestamps_list[-60:]
    graph_rendered = graph.render_data_uri()

    return graph_rendered

