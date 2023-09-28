# Auto Transfer Machine
> AutoTransferMachine转载机 - 为发光发热而生

## :triangular_flag_on_post:功能

* 批量爬取站点指定资源并下载到本地（例：可通过脚本选择爬取影站除禁转、分集外的所有资源）
* 自动从源站抓取转种需要的媒体信息，通过POST达到精确转种
* 自动生成截图（可指定数量与格式）
* 自动生成新的PTGEN与MediaINFO信息

## :warning:注意事项
* 部分有特殊MediaINFO模板的站点，以及对转出有严格要求的站点慎用

## :warning:安装说明
1. #### 安装PYTHON环境，已安装可跳过
   * 更新源 :star:
     * `sudo apt update && sudo apt upgrade`
   *    安装依赖 :star:
         * `sudo apt install -y wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev`
   * 下载安装包 :star:
     * `wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz`
   * 解压并编译 :star:
     * `tar xzf Python-3.10.0.tgz` 
     *    `cd Python-3.10.0` 
       * `./configure --enable-optimizations` 
       * `make altinstall`
   * 测试 :star:
     * `sudo python3 -m pip install --upgrade pip`
   * 删除安装包（如有需要） :star:
     * `sudo rm -rf /home/Python-3.10.0` 
     * `sudo rm /home/Python-3.10.0.tgz`

2. #### 安装ATM
   * 安装ATM依赖 :star:
     * `sudo apt-get install -y python3-pip ffmpeg mediainfo mktorrent screen unzip git`
   * 安装ATM本体:star:
     * `pip install AutoTransferMachine`
   * 设置ATM配置信息 :star:
     * `bash <(curl -s https://raw.githubusercontent.com/Ethan930717/AutoTransferMachine/main/atm/atm_install.sh)`

   #### 3.完成
## :warning:已适配转出站点

<table>
  <tr>
    <td colspan="6" align="center">:star:已适配</td>
    <td align="center">:construction_worker_man:施工中</td>
  </tr>  
  <tr>
    <td align="center">观众</td>
    <td align="center">CarPT</td> 
    <td align="center">大青虫</td> 
    <td align="center">打胶</td> 
    <td align="center">碟粉</td>     
    <td align="center">咖啡</td>     
    <td align="center">学校</td> <!-- 施工中 -->
  </tr>  
  <tr>
    <td align="center">龙之家</td>
    <td align="center">GTK</td> 
    <td align="center">海胆</td> 
    <td align="center">白兔</td> 
    <td align="center">好大</td>  
    <td align="center">铂金学院</td>    
    <td align="center">阿童木</td> <!-- 施工中 -->
  </tr> 
  <tr>
    <td align="center">自由农场</td>
    <td align="center">杜比</td> 
    <td align="center">红豆饭</td> 
    <td align="center">家园</td> 
    <td align="center">小蚂蚁</td>
    <td align="center">猫</td>     
    <td align="center">普斯特</td> <!-- 施工中 -->
  </tr> 
  <tr>
    <td align="center">明教</td>
    <td align="center">空</td> 
    <td align="center">HDTIME</td> 
    <td align="center">好多油</td> 
    <td align="center">HDVIDEO</td>
    <td align="center">铂金家</td>     
    <td align="center">蝴蝶</td> <!-- 施工中 -->
  </tr> 
  <tr>
    <td align="center">HDZONE</td> 
    <td align="center">大聪明</td> 
    <td align="center">北川</td> 
    <td align="center">冰淇淋</td>
    <td align="center">爱萝莉</td>
    <td align="center">PTLSP</td>
    <td align="center">我堡</td> <!-- 施工中 -->
  </tr> 
  <tr>
    <td align="center">ITZMX</td> 
    <td align="center">开心</td> 
    <td align="center">库非</td> 
    <td align="center">芒果</td>
    <td align="center">馒头</td>
    <td align="center">PTT</td>
    <td align="center">不可说</td> <!-- 施工中 -->
  </tr> 
  <tr>
    <td align="center">南洋</td> 
    <td align="center">OKPT</td> 
    <td align="center">奥申</td> 
    <td align="center">熊猫</td>
    <td align="center">猪猪</td>
    <td align="center">红叶</td>
    <td align="center">烧包</td> <!-- 施工中 -->
  </tr>
  <tr>
    <td align="center">肉丝</td> 
    <td align="center">聆音</td> 
    <td align="center">TCCF</td> 
    <td align="center">你堡</td>
    <td align="center">冬樱</td>
    <td align="center">52PT</td>
    <td align="center">瓷</td> <!-- 施工中 -->
  </tr>
  <tr>
    <td align="center">伊甸园</td> 
    <td align="center">1PTBA</td> 
    <td align="center">朱雀</td> 
    <td align="center">织梦</td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td> <!-- 施工中 -->
  </tr> 
</table>





