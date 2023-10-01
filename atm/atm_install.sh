#!/usr/bin/env bash
#安装python
echo "请指定一个存放目录以存放配置文件,如/home/program"
valid=false
while [ $valid = false ]
do
read dir
if [ -d $dir ]
then
valid=true
cd $dir
pwd
else
echo "输入地址有误，请重新输入！"
fi
done
cd $dir
mkdir atm
echo "创建atm文件夹成功"
cd atm
mkdir torrent_path record_path screenshot_path
echo "创建功能文件夹成功"
cat > au.yaml << EOF
basic:
  picture_num: 6                 #默认自动截图的张数，不设置就是3
  workpath: /home/atm/           #au.yaml所在文件夹的地址
  doubancookie:                  #豆瓣的cookie
  new_folder: 0                  #不用动
  check: 0                       #不用动
  picture_num: 6                 #默认自动截图的张数，不设置就是3
  workpath: /home/atm/           #au.yaml所在文件夹的地址
  new_folder: 0                  #不用动
  check: 0                       #不用动
  record_path: /home/atm/record_path           #记录类文件存放路径
  screenshot_path: /home/atm/screenshot_path   #截图暂存路径
  torrent_path: /home/atm/torrent_path         #种子下载目录
  torrent_list: /home/atm/record_path/shadowflow_torrents.xlsx   #种子信息文档路径，工具的dl指令会自动生成
  serverchan_api: SCT149************            #server酱的sendkey，发种结束后可以push推送通知
  tmdb_api:                                     #tmdb的api，没有就空着

qbinfo:
  qburl: 192.168.5.1:8080   #QB地址
  qbwebuiusername: admin    #用户名
  qbwebuipassword: admin    #密码
  start: 1                  #选1则进种自动开始，选0进种暂停，默认跳校验
image hosting:              #图床
  seq:                      #这边可以调整图床优先级顺序
    1: smms
    2: pter
    3: freeimage
    4: dahuimg
  pter:
    cookie: KEEP_LOGIN_GOAUTH=vrksE%3Aecd5c7992a32ff3***********  #cookie直接F12从控制台复制抓取即可
    url: https://s3.pterclub.com
  dahuimg:
    cookie: 
    url: https://img.dahu.fun/
  smms:
    apikey: 
  freeimage:
    cookie: 
    url: https://freeimage.host/

site info:  #站点信息,为方便大家使用，所有适配的站点全部加到了，需要的站点填上信息，然后将enable设为1即可启用
  audience:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://audiences.me/
  btschool: #学校未适配完成
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pt.btschool.club/
  carpt:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://carpt.net/
  cyanbug:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://cyanbug.net/
  dajiao:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://dajiao.cyou
  discfan:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://discfan.net/
  dragonhd:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.dragonhd.xyz/
  freefarm:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pt.0ff.cc/
  gtk:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pt.gtk.pw/
  haidan:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.haidan.video/
  hares:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://club.hares.top/
  hdarea:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hdarea.club/
  hddolby:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.hddolby.com/
  hdfans:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hdfans.org/
  hdhome:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hdhome.org/
  hdmayi:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hdmayi.com/
  hdpost: #普斯特未适配完成
    enable: 0
    cookie: ''
    uplver: 0
    url: https://pt.hdpost.top/
  hdpt:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hdpt.xyz/
  hdtime:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hdtime.org/
  hdu:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pt.hdupt.com/
  hdvideo:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hdvideo.one/
  hdzone:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hdfun.me/
  hhclub:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hhanclub.top/
  hitpt:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.hitpt.com/
  hudbt: #蝴蝶为适配完成
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://hudbt.hust.edu.cn/
  icc:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.icc2022.com/
  ilolicon:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://share.ilolicon.com/
  itzmx:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pt.itzmx.com/
  joyhd:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.joyhd.net/
  kufei:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://kufei.org/
  mangguo:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.3wmg.com/
  mteam:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://kp.m-team.cc/
  nanyang:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://nanyangpt.com/
  okpt:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.okpt.net/
  oshen:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.oshen.win/
  pandapt:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pandapt.net/
  piggo:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://piggo.me/
  ptcafe:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://ptcafe.club/
  ptchina:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://ptchina.org/
  pter:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pterclub.com/
  pthome:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.pthome.net/
  ptlsp:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.ptlsp.com/
  ptsbao: #烧包未适配完成
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://ptsbao.club/
  pttime:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://www.pttime.org/t
  redleaves:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://leaves.red/
  rousi:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://rousi.zip/
  shadowflow:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://shadowflow.org/
  soulvoice:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pt.soulvoice.club/
  tccf:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://et8.org/
  ubits:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://ubits.club/
  wintersakura:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://wintersakura.net/
  wuerpt:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://52pt.site/
  ydy:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://pt.hdbd.us/
  yiptba:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://1ptba.com/
  zhuque:   #朱雀需要另外添加torrentkey，在朱雀个人信息中可以查看
    enable: 0
    cookie: ''
    torrentkey: ''
    uplver: 0
    url: https://zhuque.in/
  zmpt:
    enable: 0
    cookie: ''
    passkey: ''
    uplver: 0
    url: https://zmpt.cc/

#以下是转种的资源信息，了解为主，脚本会自动生成
path info:
  path1:
    downloadpath: /download #这里是QB内部的下载地址
    enable: 1 #这里选择本种是否启动，选0则会跳过这个种
    collection: 1 #这里默认1即可，是打包发布的意思
    path: /home/media/黑鹰坠落.Black.Hawk.Down.2001.1080p.AMZN.WEB-DL.H264.DDP5.1-YingWEB #写的是资源在机器上的文件夹地址
    uploadname: Black Hawk Down 2001 1080p AMZN WEB-DL H264 DDP5.1-YingWEB #这条是主标题，会适配自动生成，也可以手写
    filename: '[Shadow].黑鹰坠落.Black.Hawk.Down.2001.1080p.AMZN.WEB-DL.H264.DDP5.1-YingWEB.torrent' 
   这里是种子文件名，所有资源的种子都要放在torrent_file文件夹里，建议直接从源站下载好，种子名字要跟资源名字相匹配
    chinesename: 黑鹰坠落     #资源中文名，用于抓豆瓣链接
    englishname: 'Black Hawk Down '  #同上，这些都会适配自动生成
    small_descr: '黑鹰坠落/黑鹰15小时/黑鹰计划/黑鹰降落 | 类型:动作 主演:乔什·哈奈特/伊万·麦克格雷格/汤姆·塞兹摩尔 [英语|内封中字]'       #副标题，也是从源站抓取自动生成
    tags: 官方 中字    #标签，同上
    sub: YingWEB    #制作组，从主标题抓取，自动生成
    type: movie   #类型，同上
    contenthead: #这里写简介头的内容，也就是感谢发布的位置
    contenttail:  #这里写简介尾的内容，适用性较少
    audio_format: DDP5.1   #音频
    video_format: H264     #视频
    medium: WEB-DL   #媒介
    source: WEB-DL   #来源
    doubanurl: https://movie.douban.com/subject/1291824/ #不写豆瓣链接则会自动抓取
    screenshot: null #如果需要自选截图，则这边直接复制图片链接即可,长度随意，注意要把basic_num数量改为0，否则默认还是会自动截图
    from_url: https://mikanani.me/
    imdb_url: null
EOF
echo "创建yaml配置模板成功，创建启动指令文件"
cd /usr/local/bin/
sudo tee atm > /dev/null << EOF
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
from AutoTransferMachine.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
EOF
sudo chmod a+x /usr/local/bin/atm
sudo apt-get install dos2unix
sudo dos2unix /usr/local/bin/atm
echo "创建成功，尝试第一次启动ATM"
atm -h








