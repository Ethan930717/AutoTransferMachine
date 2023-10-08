import argparse
import os


def readargs():
    mainpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yaml_path = os.path.join(mainpath,"au.yaml")
    parser = argparse.ArgumentParser(description='欢迎使用大胡开发的ATM自动转种机，如果你有意和我一起开发和测试本工具，欢迎你加入ATM研发群870081858')
    parser.add_argument('-yp','--yaml-path', type=str, help='指定你的au.yaml路径',required=True,default=yaml_path)
    args = parser.parse_args()
    return args
