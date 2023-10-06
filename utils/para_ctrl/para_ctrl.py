from utils.para_ctrl.readyaml import readyaml
from utils.para_ctrl.readargs import readargs
from utils.para_ctrl.readyaml import write_yaml

import os
from loguru import logger
import csv
import urllib
def choose_function():
    print("请选择你想要执行的功能：")
    print(f"1. 自动转种模式(从本地抓取种子上传）")
    print(f"2. 发种模式(适用于发布自己的资源，自动制种，而不是转发其他资源)")
    print("3. 签到模式")
    print("4. 拉种模式")
    print("5. pathinfo模板转换")
    print("6. 自动截图并上传图床")
    print("脚本运行过程中，可使用ctrl+c退出")
    modechoice = input("请输入你的选择：")
    return modechoice

def read_para():
    args = readargs()
    modechoice=choose_function()
    iu=0#img upload
    su=0#sign
    ru=0#resources upload
    au_data  = readyaml(args.yaml_path)
    if 'basic' in au_data and 'workpath' in au_data['basic']:
        if not os.path.exists(au_data['basic']['workpath']):
            logger.info('检测到workpath目录并未创建，正在新建文件夹：'+au_data['basic']['workpath'])
            os.makedirs(au_data['basic']['workpath'])
        itemlist=['record_path','screenshot_path']
        for item in itemlist:
            if not item in au_data['basic']:
                au_data['basic'][item]=os.path.join(au_data['basic']['workpath'],item)
                if not os.path.exists(au_data['basic'][item]):
                    logger.info('检测到'+item+'目录并未创建，正在新建文件夹：'+au_data['basic'][item])
                    os.makedirs(au_data['basic'][item])

    au_data['yaml_path']=args.yaml_path
    write_yaml(au_data)
    if modechoice == "1":
        au_data['mod']='transfer'
    elif modechoice == "2":
        au_data['mod']='upload'
    elif modechoice == "3":
        au_data['mod']='sign'
    elif modechoice == "4":
        au_data['mod']='download'
    elif modechoice == "5":
        au_data['mod']='transinfo'
    else:
        logger.error('模式选择有误，请重试')
        raise ValueError('模式选择有误，请重试')

    if modechoice == "1":
        if not 'path info' in au_data or len(au_data['path info'])==0:
            logger.error('参数输入错误，发布资源请至少输入一个本地文件地址')
            raise ValueError ('参数输入错误，发布资源请至少输入一个本地文件地址')
        for item in au_data['path info']:
            if not 'path' in au_data['path info'][item] or au_data['path info'][item]['path']==None or au_data['path info'][item]['path']=='':
                logger.error('参数输入错误，'+item+'请至少输入一个本地文件地址')
                raise ValueError ('参数输入错误，'+item+'请至少输入一个本地文件地址')
            if 'type' in au_data['path info'][item] and not ( 'anime' in au_data['path info'][item]['type'].lower() or 'tv' in au_data['path info'][item]['type'].lower() or 'movie' in au_data['path info'][item]['type'].lower() or 'doc' in au_data['path info'][item]['type'].lower()):
                logger.error('参数输入错误，'+item+'的type类型暂不支持')
                raise ValueError ('参数输入错误，'+item+'的type类型暂不支持')
        if not 'qbinfo' in au_data:
            logger.error('参数输入错误，未找到qbinfo')
            raise ValueError ('参数输入错误，未找到qbinfo')
        if not 'start' in au_data['qbinfo'] or not (int(au_data['qbinfo']['start'])==1 or int(au_data['qbinfo']['start'])==0):
            au_data['qbinfo']['start']=0
            logger.warning('未找到qbinfo中的start(添加到qb的种子是否自动开始)参数,已设置为0(不自动开始)')

    return au_data



