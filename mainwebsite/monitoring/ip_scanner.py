import subprocess, os, multiprocess
import platform

current_os = platform.system()
device_list = []


def pinger(job_q, results_q):
    DEVNULL = open(os.devnull, 'w')
    while True:
        ip = job_q.get()
        if ip is None:
            break
        try:
            if current_os == 'Windows':
                subprocess.check_call(['ping', '-n', '1', '-w', '500', ip], stdout=DEVNULL)
            else:
                subprocess.check_call(['ping', '-c1', ip], stdout=DEVNULL)

            results_q.put(ip)
        except:
            pass


def ip_scanner(ip):
    pool_size = 255
    jobs = multiprocess.Queue()
    results = multiprocess.Queue()
    pool = [multiprocess.Process(target=pinger, args=(jobs, results))
            for i in range(pool_size)]
    for p in pool:
        p.start()
    for i in range(1, 255):
        jobs.put(ip + '{0}'.format(i))
    for p in pool:
        jobs.put(None)
    for p in pool:
        p.join()
    while not results.empty():
        ip = results.get()
        device_list.append(ip)
