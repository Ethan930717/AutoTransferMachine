#!/usr/bin/env bash
echo "请输入您本地的视频文件存放目录,如/home/media"
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
parent=$(dirname "$dir")
atm="$parent/atm"
mkdir -p "$atm"
echo "创建atm文件夹成功"
cd atm
curl -o "$atm/atm.zip" https://pan.dahu.fun/d/file/atm.zip?sign=yjLNnG5S4oD21ZIIC-0y02CFZSRq5TJAccdhRtfKVeQ=:0
unzip "$atm/atm.zip" -d "$atm"
cd $atm
echo "atm配置文件加载成功，您的视频文件夹路径前级已变更为atm"
docker-compose run atm








