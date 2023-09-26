import argparse
import os


def readargs():
    mainpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yaml_path = os.path.join(mainpath,"au.yaml")
    basic_path = os.path.join(mainpath,"basicinfo.yaml")
    torrent_list = os.path.join(mainpath,"torrentlist.txt")
    parser = argparse.ArgumentParser(description='欢迎使用ATM自动转种机，交流Q群870081858，请自备最新的PTPP截图申请入群，进群需验证发种总数超过100')

    parser.add_argument('-u','--upload', action='store_true', default=False, help='自动转种模式')
    parser.add_argument('-s','--sign', action='store_true', default=False, help='自动登陆模式')
    parser.add_argument('-dl', '--download', action='store_true', default=None, help='拉种模式')
    parser.add_argument('-iu','--img-upload', action='store_true', default=False, help='使用图片链接转发图床')
    parser.add_argument('-di','--douban-info', action='store_true', default=False, help='获取豆瓣信息')
    parser.add_argument('-mi','--media-img', action='store_true', default=False, help='自动截图并上传图床')
    parser.add_argument('-ih','--img-host', type=str, help='选择你想要上传的图床. [dahuimg,smms,pter,freeimage],默认使用猫站图床',choices=['smms','pter','freeimage','dahuimg'],required=False,default='pter')
    parser.add_argument('-if','--img-file', nargs='+',help='指定图片路径',action='append',required=False)
    parser.add_argument('-iform','--img-form', help='指定返回的图床链接格式. [bbcode,img]',choices=['bbcode','img'],required=False,default='img')
    parser.add_argument('-du','--douban-url', type=str, help='指定豆瓣资源链接',required=False,default='')
    parser.add_argument('-mf','--media-file', type=str, help='指定媒体路径',required=False,default='')
    parser.add_argument('-in','--img-num', type=int, help='指定上传图片数量,默认三张',required=False,default=3)
    parser.add_argument('-yp','--yaml-path', type=str, help='指定你的au.yaml路径',required=True,default=yaml_path)
    parser.add_argument('-bp','--basic-path', type=str, help='指定你的basicinfo.yaml路径',required=False,default=basic_path)
    args = parser.parse_args()
    return args
