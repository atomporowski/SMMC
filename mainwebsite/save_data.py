import os


def save_data_to_file(data_to_save, save_path, file_name):
    complete_path = save_path + file_name + '.txt'
    print(complete_path)
    f = open(complete_path, 'w+')
    data_to_save = map(lambda x: x + '\n', data_to_save)
    f.writelines(data_to_save)
    f.close()


def create_win_ini(data_to_save, save_path, file_name):
    complete_path = save_path + file_name + '.ini'
    if os.path.exists(complete_path):
        os.remove(complete_path)
    f = open(complete_path, 'w+')
    f.writelines('[win]\n')
    for i in data_to_save:
        f.writelines(i + '\n')

    file_context = f'''
[win:vars]
ansible_port=5986
ansible_connection=winrm
ansible_winrm_scheme=https
ansible_winrm_server_cert_validation=ignore
ansible_winrm_kerberos_delegation=true'''
    f.writelines(file_context)
    f.close()

