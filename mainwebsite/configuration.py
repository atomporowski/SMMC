import os

from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user

from . import save_data
from .datamodels import *
import re

configuration = Blueprint('configuration', __name__)

regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

@configuration.route('/configuration', methods=['GET', 'POST'])
@login_required
def network_configuration():
    if request.method == 'POST':
        user_id = current_user.id
        network_ip = request.form.get('ip_address')
        adm_login = request.form.get('admin_login')
        adm_pass = request.form.get('admin_password')
        # TODO: We need to check if one user has only one config
        if re.search(regex, str(network_ip)):
            pass
        else:
            flash('IP address is not valid.', category='error')

        # Checking if user entered data
        if network_ip == "" or adm_pass == "" or adm_login == "":
            flash("No data to save!")
            return redirect('/configuration')

        # Ability to save new data or edit existing one
        new_configuration = Config(user_id=user_id, network_ip=network_ip, adm_login=adm_login, adm_pass=adm_pass)
        if Config.query.filter_by(user_id=current_user.id).first():
            Config.query.filter_by(user_id=current_user.id).update({"network_ip": network_ip, "adm_login": adm_login,
                                                                    "adm_pass": adm_pass})
            db.session.commit()
            flash('Configuration updated!', category='success')
        else:
            db.session.add(new_configuration)
            db.session.commit()
            flash('Configuration saved!', category='success')
    curr_config = config_return()
    return render_template("configuration.html", user=current_user, curr_config=curr_config)


@configuration.route('/configuration/deleteserverconf', methods=['GET', 'POST'])
@login_required
def configuration_delete():
    configuration_to_delete = Config.query.filter_by(user_id=current_user.id).first()

    try:
        db.session.delete(configuration_to_delete)
        db.session.commit()
        flash("Configuration deleted successfully", category='success')
        return redirect('/configuration')
    except:
        flash("There is no configuration!")
        return redirect('/configuration')


@configuration.route('/configuration/emailsenderconf', methods=['GET', 'POST'])
@login_required
def email_sender_save():
    if request.method == 'POST':
        user_id = current_user.id
        email_account = request.form.get('email_account')
        email_account_password = request.form.get('email_account_password')
        smtp_email_account = request.form.get('smtp_email_account')
        email_account_port = request.form.get('email_account_port')
        monitoring_server_ip = request.form.get('monitoring_server_ip')
        data_to_file = [email_account, email_account_password, smtp_email_account, email_account_port,
                        monitoring_server_ip]

        email_conf = Email_config.query.filter_by(user_id=current_user.id)

        save_path = 'mainwebsite/monitoring/'
        file_name = 'monitoring'

        if email_account == "" or email_account_password == "" or smtp_email_account == "" or \
                email_account_port == "" or monitoring_server_ip == "":
            flash("No data to save!", category='error')
            return redirect('/configuration')

        email_sender_conf = Email_config(user_id=user_id, email_account=email_account,
                                         email_account_password=email_account_password,
                                         smtp_email_account=smtp_email_account, email_account_port=email_account_port,
                                         monitoring_server_ip=monitoring_server_ip)

        if email_conf.first():
            email_conf.update({'email_account': email_account, 'email_account_password': email_account_password,
                               'smtp_email_account': smtp_email_account, 'email_account_port': email_account_port,
                               'monitoring_server_ip': monitoring_server_ip})
            save_data.save_data_to_file(data_to_file, save_path, file_name)
            db.session.commit()
            flash('E-mail configuration updated', category='success')
        else:
            save_data.save_data_to_file(data_to_file, save_path, file_name)
            db.session.add(email_sender_conf)
            db.session.commit()
            flash('E-mail sender configuration saved!', category='success')
        return redirect('/configuration')

    curr_config = config_return()
    return render_template("configuration.html", user=current_user, curr_config=curr_config)


@configuration.route('/configuration/deletemailconf', methods=['GET', 'POST'])
@login_required
def mail_configuration_delete():
    email_conf_to_delete = Email_config.query.filter_by(user_id=current_user.id).first()

    try:
        if os.path.exists('mainwebsite/monitoring/monitoring.txt'):
            os.remove('mainwebsite/monitoring/monitoring.txt')
        else:
            flash('There is no file to delete!')
        db.session.delete(email_conf_to_delete)
        db.session.commit()
        flash("E-mail configuration deleted successfully", category='success')
        return redirect('/configuration')
    except:
        flash("There is no E-mail configuration!")
        return redirect('/configuration')


def config_return():
    server_conf = Config.query.filter_by(user_id=current_user.id).first()
    email_conf = Email_config.query.filter_by(user_id=current_user.id).first()
    print("server: ", server_conf)
    print("email: ", email_conf)
    if email_conf and server_conf:
        curr_config = {
            'network_ip': server_conf.network_ip,
            'adm_login': server_conf.adm_login,
            'adm_pass': server_conf.adm_pass,
            'email_account': email_conf.email_account,
            'email_account_password': email_conf.email_account_password,
            'smtp_email_account': email_conf.smtp_email_account,
            'email_account_port': email_conf.email_account_port,
            'monitoring_server_ip': email_conf.monitoring_server_ip
        }
    elif server_conf:
        curr_config = {
            'network_ip': server_conf.network_ip,
            'adm_login': server_conf.adm_login,
            'adm_pass': server_conf.adm_pass,
            'email_account': 'No data entered',
            'email_account_password': 'No data entered',
            'smtp_email_account': 'No data entered',
            'email_account_port': 'No data entered',
            'monitoring_server_ip': 'No data entered'
        }
    elif email_conf:
        curr_config = {
            'network_ip': 'No data entered',
            'adm_login': 'No data entered',
            'adm_pass': 'No data entered',
            'email_account': email_conf.email_account,
            'email_account_password': email_conf.email_account_password,
            'smtp_email_account': email_conf.smtp_email_account,
            'email_account_port': email_conf.email_account_port,
            'monitoring_server_ip': email_conf.monitoring_server_ip
        }

    else:
        curr_config = False
    print(curr_config)
    return curr_config
