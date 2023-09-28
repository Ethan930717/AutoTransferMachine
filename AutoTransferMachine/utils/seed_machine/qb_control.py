import subprocess
import time
import qbittorrentapi
import os
screen_path = os.popen("which screen").read().strip()
query = subprocess.run([screen_path, "-Q", "-S", "fa", "select"], capture_output=True, text=True)
client = qbittorrentapi.Client(host=qbinfo['qburl'],username=qbinfo['qbwebuiusername'],password=qbinfo['qbwebuipassword'])
upload_max = 100 * 1024 * 1024  #达到100Mb/s后暂停发种
upload_min = 90 * 1024 * 1024   #小于90Mb/s后继续发种
paused = False # flag of paused status
while True:
    try:
        query.check_returncode()
        print(query.stdout)
        ps = subprocess.run(["ps", "-C", "AutoTransferMachine", "-o", "pid,stat"], capture_output=True, text=True)
        ps.check_returncode()
        lines = ps.stdout.split("\n")
        columns = lines[1].split()
        stat = columns[1]
        print(stat)
    except subprocess.CalledProcessError as e:
        print("子进程执行失败，错误信息如下：")
        print(e)
    current_upload = client.transfer.info.up_info_speed
    if current_upload >= upload_max:
        if "S" in stat: # 如果脚本在运行
            subprocess.run(["screen", "-X", "-S", "fa", "stuff", "^z"])
            print("达到最大上传速度，暂停发种")
            paused = True 
        else: # 如果脚本没有运行
            print("AutoTransferMachine处于暂停状态")
    elif current_upload < upload_min:
        if "T" in stat: # 如果脚本处于暂停状态
            subprocess.run(["screen", "-X", "-S", "fa", "stuff", "fg\n"])
            print("上传速度空闲，继续发种")
            paused = False # set paused flag to False
        else: 
            print("AutoTransferMachine处于运行状态")
    print("当前的实时上传速率为 " + str(round(current_upload / (1024 * 1024), 2)) + " MB/s")
    time.sleep(10)
