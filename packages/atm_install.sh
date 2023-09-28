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
echo "检查安装环境"
sudo rm -rf /usr/local/lib/python3.10/dist-packages/AutoTransferMachine
sudo rm /usr/local/bin/atm
echo "开始安装"
sudo apt update && sudo apt upgrade
sudo apt install -y wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar xzf Python-3.10.0.tgz
echo "编译python"
cd Python-3.10.0
./configure --enable-optimizations
make altinstall
echo "删除安装包"
sudo rm -rf $dir/Python-3.10.0
sudo rm $dir/Python-3.10.0.tgz
sudo python3 -m pip install --upgrade pip
echo "从Git克隆项目"
cd $dir
git clone https://github.com/Ethan930717/AutoTransferMachine.git AutoTransferMachine
echo "安装ATM依赖"
sudo apt-get install -y python3-pip screen unzip git
pip install ffmpeg mediainfo maketorrent loguru pyyaml doubaninfo pip install loguru pyyaml doubaninfo requests beautifulsoup4 lxml cloudscraper qbittorrent-api

echo "转移openpyxl包"
cd $dir/AutoTransferMachine/packages
unzip -o openpyxl.zip -d /usr/local/lib/python3.10/dist-packages/
echo "删除openpyxl压缩包"
sudo rm openpyxl.zip
echo "生成转种配置文件"
unzip -o atm.zip -d $dir/atm
echo "删除配置文件压缩包"
sudo rm atm.zip
echo "转移命令行配置"
mv atm /usr/local/bin/
chmod +x /usr/local/bin/atm
echo "转移ATM包"
cd $dir
mv AutoTransferMachine /usr/local/lib/python3.10/dist-packages/
echo "删除package文件夹"
sudo rm packages
echo "测试运行情况"
atm -h






