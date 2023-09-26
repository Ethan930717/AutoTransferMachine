from loguru import logger
import json
import os.path
class site(object):
    def __init__(self,sitename,sitedict):
        self.sitename   = sitename
        self.exist_url   = False
        self.exist_cookie=False
        self.exist_passkey=False
        self.uplver =1
        self.enable =0
        self.check = False
        self.mediainfo_template_file=''
        self.passkey=''
        self.token='' #zhuque站点token
        self.torrentkey='' #zhuque站点torrentkey

        try:
            self.uplver =int(sitedict['uplver'])
        except:
            logger.warning(sitename+'站点匿名发布uplver信息填错错误，已设置为1:默认匿名发布')
            self.uplver =1
            sitedict['uplver']=1
        if not (self.uplver==0 or self.uplver==1):
            logger.warning(sitename+'站点匿名发布uplver信息填错错误，已设置为1:默认匿名发布')
            self.uplver =1
            sitedict['uplver']=1

        if 'mediainfo_template_file' in sitedict and sitedict['mediainfo_template_file']!= None and sitedict['mediainfo_template_file'].strip()!='':
            if os.path.exists(sitedict['mediainfo_template_file']):
                self.mediainfo_template_file=sitedict['mediainfo_template_file']
            else:
                raise Exception(sitename+'站点的mediainfo模板文件不存在')
        else:
            self.mediainfo_template_file=''


        try:
            self.enable =int(sitedict['enable'])
        except:
            logger.warning(sitename+'站点enable信息填错错误，已设置为0:关闭')
            self.enable =0
            sitedict['enable']=0

        if not (self.enable==0 or self.enable==1):
            logger.warning(sitename+'站点匿名发布enable信息填错错误，已设置为0:关闭')
            self.enable =0
            sitedict['enable']=0

        if 'url' in sitedict :
            self.url=sitedict['url']
            self.exist_url=True
        else:
            self.url=''
            self.exist_url=False


        if 'cookie' in sitedict :
            self.cookie=sitedict['cookie']
            self.exist_cookie=True
        else:
            self.cookie=''
            self.exist_cookie=False

        if 'passkey' in sitedict :
            self.passkey=sitedict['passkey']
            self.exist_passkey=True
        else:
            self.passkey=''
            self.exist_passkey=False

        if 'check' in sitedict :
            if str(sitedict['check']=='1'):
                self.check=True
            else:
                self.check=False

        if sitename=='zhuque':
            if 'torrentkey' in sitedict :
                self.torrentkey=sitedict['torrentkey']
            else:
                logger.warning('zhuque站点缺少torrentkey，将会导致无法做种')

        if self.enable==1 and not self.exist_cookie:
            logger.error('未找到'+sitename+' 站点的cookie信息')
            raise ValueError ('未找到'+sitename+' 站点的cookie信息')


    def print(self):
        from AutoTransferMachine.utils.getinfo.torrent_download import fromsite
        print('Site info:')
        print('sitename:'  ,self.sitename  )
        print('enable:'    ,self.enable    )
        print('url:'       ,self.url       )
        print('loginurl:'  ,self.loginurl  )
        print('uploadurl:' ,self.uploadurl )
        sitename = self.sitename
        if self.exist_url:
            url = self.url
            print('url:',self.url)
        else:
            print('站点地址:未设置或未识别')
        if self.exist_cookie:
            cookies = self.cookie
            print('cookie:',self.cookie)
        else:
            print('cookiefile:未设置或未识别')
        if self.exist_passkey:
            passkey = self.passkey
            print('passkey:',self.passkey)
        else:
            print('passkey:未设置或未识别')
        fromsite(url,cookie,passkey,sitename)
        print('')

def makesites(siteinfo):
    sites=dict()
    for item in siteinfo:
        sites[item]=site(item,siteinfo[item])
    return sites








