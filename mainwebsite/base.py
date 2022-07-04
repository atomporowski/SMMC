import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, request, render_template, flash, redirect, send_file
from flask_login import current_user

base = Blueprint('base', __name__)


@base.route('/base', methods=['POST'])
def send_request():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    message_from_client = request.form.get("message")

    message = MIMEMultipart()
    message['From'] = email
    message['Subject'] = 'Question From Website from: ' + first_name + " " + last_name
    message.attach(
        MIMEText("Message:" + "\n" + message_from_client + "\n" + first_name + " " + last_name + "\n" + email))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("servermmcenter@gmail.com", "lkfa wzky wlku eraj")
        server.sendmail(email, "servermmcenter@gmail.com", message.as_string())

        flash("Your message has been sent. Thank You!")
        return render_template('home.html', user=current_user)
    except:
        flash('There is a problem with sending message!', category='error')
        return render_template('home.html', user=current_user)


@base.route('/base/download', methods=['GET', 'POST'])
def download_file():
    file_name = "manual"
    file_path = "./static/"
    path = file_path + file_name + ".pdf"

    return send_file(path, as_attachment=True)



