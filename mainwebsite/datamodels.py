from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    company = db.Column(db.String(100))
    phone = db.Column(db.String(30))


class Config(db.Model):
    __tablename__ = 'configuration'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    network_ip = db.Column(db.String(15))
    adm_login = db.Column(db.String(150))
    adm_pass = db.Column(db.String(150))


class Email_config(db.Model):
    __tablename__ = 'email_config'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    email_account = db.Column(db.String(150))
    email_account_password = db.Column(db.String(150))
    smtp_email_account = db.Column(db.String(150))
    email_account_port = db.Column(db.String(4))
    monitoring_server_ip = db.Column(db.String(15))


class Monitoring(db.Model):
    __tablename__ = 'monitoring'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    server_ip = db.Column(db.String(15))


class Clients_data(db.Model):
    __tablename__ = 'clients_data'
    id = db.Column(db.Integer, primary_key=True)
    # I think we must remove user_id and think of other way to bind data to the client
    # user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    server_ip = db.Column(db.String(50))
    hostname = db.Column(db.String(30))
    os = db.Column(db.String(15))
    boot_time = db.Column(db.String(24))
    cpu_percent = db.Column(db.Integer)
    memory_percent = db.Column(db.Integer)
    virtual_mem = db.Column(db.Integer)
    avg_load = db.Column(db.Integer)
    timestamp = db.Column(db.String(24))
