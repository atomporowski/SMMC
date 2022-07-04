import socket, psutil, time, pickle, datetime, platform, smtplib, linecache

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HEADER = 64
PORT = 6464
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = linecache.getline('monitoring.txt', 5).rstrip('\n')
ADDR = (SERVER, PORT)
Data = {}
temp = 0

# AF_INET = IPv4, SOCK_STREAM = TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def raise_alert(hostname, resource, resource_usage):
    email = linecache.getline('monitoring.txt', 1).rstrip('\n')

    resource_usage_to_string = str(resource_usage)
    timestamp = datetime.time()
    print(timestamp)
    timestamp_to_string = timestamp.strftime("%m/%d/%Y, %H:%M:%S")

    message = MIMEMultipart()
    message["From"] = email
    message["Subject"] = hostname + ' ' + resource + ' alert detected.'
    message.attach(MIMEText(
        "Alert details: " + "\n" + hostname + "\n" + resource + ' ' + resource_usage_to_string + "\n" + "Alert detected at: " + timestamp_to_string))

    server = smtplib.SMTP(linecache.getline('monitoring.txt', 3).rstrip('\n'),
                          linecache.getline('monitoring.txt', 4).rstrip('\n'))
    server.starttls()
    server.login(email, linecache.getline('monitoring.txt', 2).rstrip('\n'))
    server.sendmail(email, email, message.as_string())


def check_high_resources(hostname, resource, resource_usage, timestamp):
    warning_counter = 0
    critical_counter = 0
    if resource_usage >= 90 and resource_usage < 95:
        warning_counter += 1
        if warning_counter == 1 or warning_counter % 10 == 0:
            raise_alert(hostname, resource, resource_usage)
    elif resource_usage >= 95:
        critical_counter += 1
        if critical_counter == 1 or critical_counter % 10 == 0:
            raise_alert(hostname, resource, resource_usage)


def check_low_resources(hostname, resource, resource_usage, timestamp):
    warning_counter = 0
    critical_counter = 0
    if resource_usage >= 10 and resource_usage < 15:
        warning_counter += 1
        if warning_counter == 1 or warning_counter % 10 == 0:
            raise_alert(hostname, resource, resource_usage)
    elif resource_usage >= 15:
        critical_counter += 1
        if critical_counter == 1 or critical_counter % 10 == 0:
            raise_alert(hostname, resource, resource_usage)


def check_uptime(hostname, resource, resource_usage, timestamp):
    now = datetime.datetime.now()
    print(resource_usage, now)
    # if(timestamp)


def check_resources():
    hostname = socket.gethostname()
    os = platform.system()
    local_ip = client.getsockname()[0]
    boot_time = psutil.boot_time()
    cpu_percent = psutil.cpu_percent(5)
    memory_percent = psutil.virtual_memory().percent
    virtual_mem = psutil.virtual_memory().percent
    avg_load = psutil.getloadavg()
    timestamp = time.time()

    data = {
        'hostname': hostname,
        'os': os,
        'ip': local_ip,
        'boot_time': datetime.datetime.fromtimestamp(boot_time).strftime('%c'),
        'cpu_percent': cpu_percent,
        'memory_percent': memory_percent,
        'virtual_mem': virtual_mem,
        'avg_load': avg_load[2],
        'timestamp': datetime.datetime.fromtimestamp(timestamp).strftime('%c')
    }

    check_high_resources(hostname, "cpu_usage", cpu_percent,
                         datetime.datetime.fromtimestamp(timestamp).strftime("%b %d %H:%M:%S %Y"))
    check_high_resources(hostname, "memory_usage", memory_percent,
                         datetime.datetime.fromtimestamp(timestamp).strftime("%b %d %H:%M:%S %Y"))
    check_high_resources(hostname, "virtual_usage", virtual_mem,
                         datetime.datetime.fromtimestamp(timestamp).strftime("%b %d %H:%M:%S %Y"))
    check_low_resources(hostname, "avg_load", avg_load[2],
                        datetime.datetime.fromtimestamp(timestamp).strftime("%b %d %H:%M:%S %Y"))
    check_uptime(hostname, "boot_time", boot_time,
                 datetime.datetime.fromtimestamp(timestamp).strftime("%b %d %H:%M:%S %Y"))
    return data


def send():
    while True:
        data_string = pickle.dumps(check_resources())
        client.send(data_string)
        time.sleep(60)


send()
