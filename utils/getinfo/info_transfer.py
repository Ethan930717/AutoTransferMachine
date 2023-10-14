import lxml
import cloudscraper
from lxml import etree
import requests
from requests.cookies import cookiejar_from_dict
from loguru import logger
import re
import os
from utils.getinfo.shadowflow_download import shadowflow_trans
from utils.getinfo.hhclub_download import hhclub_trans


def cookies_raw2jar(raw_cookies): # 定义一个函数，将原始的cookie字符串转换为cookiejar对象
    cookie_dict = {}
    for cookie in raw_cookies.split(";"):
        key, value = cookie.split("=", 1)
        cookie_dict[key] = value
    return cookiejar_from_dict(cookie_dict) # 调用requests模块中的函数

def getmediainfo(yamlinfo):
    csv_dir = yamlinfo['basic']['record_path']
    while True:
        # 列出目录下的所有CSV文件
        csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
        if not csv_files:
            print("在指定目录下没有找到任何CSV文件。")
            return
        # 打印CSV文件列表供用户选择
        for idx, filename in enumerate(csv_files, start=1):
            print(f"{idx}. {filename}")
        # 获取用户选择
        choice = input("请选择一个CSV文件（输入对应的序号，或者输入'q'退出）：")
        if choice.lower() == 'q':
            return
        try:
            selected_file = csv_files[int(choice) - 1]
        except (ValueError, IndexError):
            print("输入无效。")
            continue
        csv_filepath = os.path.join(csv_dir, selected_file)
        if "shadowflow" in selected_file:
            print("已选择对影的资源进行模板转换。")
            shadowflow_trans(yamlinfo,csv_filepath)
            return
        elif "hhclub" in selected_file:
            print("已选择对憨憨的资源进行模板转换。")
            hhclub_trans(yamlinfo,csv_filepath)
            return
        else:
            print("选择的文件暂不支持模板转换，请重新选择。")
            continue






