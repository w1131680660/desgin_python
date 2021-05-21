import os,requests

def master_upload_file(files,file_path):
    url = 'https://www.beyoung.group/file_upload/'
    path2 = os.path.join(r'operation/operating_data/', file_path, )
    data = {'path':path2}
    print(data)
    res =requests.post(url,data,files={'file':files})
    path3=  os.path.join(r'operation/operating_data/',file_path, str(files))
    print('这是什么路径\n',path3)
    return path3


def bug_upload(files,file_path):
    url = 'https://www.beyoung.group/file_upload/'
    # url = 'http://106.53.250.215:9128/file_upload/'
    import time
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    path2 = os.path.join(r'task_distribution/', "%s/"%file_path,date )
    data = {'path':path2}
    print(data)
    res =requests.post(url,data,files={'file':files})
    path3=  os.path.join(r'task_distribution/',"%s/"%file_path, "%s/"%(date),str(files))
    print('这是什么路径\n',path3)
    return path3

