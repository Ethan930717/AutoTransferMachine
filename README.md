<h1 align="center"> ⭐️ Auto Transfer Machine ⭐️ </h1>
<h2 align="center"><strong>:heart_on_fire:为发光发热而生:heart_on_fire:</a></strong></h2>

## :triangular_flag_on_post:功能

* 批量爬取站点指定资源并下载到本地（例：可通过脚本选择爬取影站除禁转、分集外的所有资源）
* 自动从源站抓取转种需要的媒体信息，通过POST达到精确转种
* 自动生成截图（可指定数量与格式）
* 自动生成新的PTGEN与MediaINFO信息

## :warning:注意事项
* 部分有特殊MediaINFO模板的站点，以及对转出有严格要求的站点慎用

## :warning:安装说明
1. #### 安装Docker以及Docker-compose环境 :star:
     * `curl -fsSL https://get.docker.com -o get-docker.sh`
     * `sudo sh get-docker.sh`
     * `sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

2. #### 拉取镜像 :star:
     * `docker pull hudan717/atm`

3. #### 加载ATM配置文档及启动 :star:
     * 把atm文件夹下载到你的机器中的任意位置，里面分别有三个子文件夹，里面各有一个占位的空文件，下载以后可以删除也可以不用理会
     * 下载以后，自行修改compose中的媒体映射路径
     * 在compose所在路径下，启动容器 `docker-compose run atm`
     * :star:请注意，要用 `docker-compose run` 不能用 `docker-compose up`
* 容器启动后会自动进入内部的/app路径，输入./a即可开启脚本
   
  ## :warning:使用说明

* 使用建议
     * 容器的运行建议跑在screen下，以下给出最基本的screen操作流程
     * `sudo apt-get install screen` 安装screen
     * `screen -R atm` 创建一个名为atm的screen(可以理解成windows的分屏)
     * 在atm分屏中开启脚本后，你可以通过ctrl+a+d退出atm的screen，回到ssh主界面进行别的操作
     * 如果要回去看看脚本的工作进度，可以使用`screen -r atm` 或者 `screen -D -r atm`指令切换回screen
     * 脚本运行过程中，你可以通过`ctrl+z`随时暂停脚本,同时在暂停状态下，你也可以通过输入`fg`让脚本继续工作


* 工作逻辑

         :arrow_down:1.从站点批量获取资源信息，将信息保存在record_path目录，并将种子下载保存至torrent_path目录

         :writing_hand:2.通过第一步获取的资源链接，批量生成转载信息，自动生成模板写入yaml的path info中

         :arrow_heading_up:3.通过第二步生成的模板，实现资源转发（若本地已有资源，可自行编辑yaml直接进行转发）


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
<br>

<h1 align="center"> ️:gift_heart: 特别感谢 :gift_heart: </h1>

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
| [<img src="https://avatars.githubusercontent.com/u/17682201?v=4" width="175px;"/><br /><sub><b>莫与</b></sub>](https://github.com/dongshuyan)  <br /> | [<img src="https://avatars.githubusercontent.com/u/32202634?v=4" width="175px;"/><br /><sub><b>明日</b></sub>](https://github.com/tomorrow505/)<br /> | [<img src="https://avatars.githubusercontent.com/u/53997080?v=4" width="175px;"/><br /><sub><b>大卫</b></sub>](https://github.com/ledccn)<br /> | [<img src="https://avatars.githubusercontent.com/u/103914473?v=4" width="175px;"/><br /><sub><b>贾佬</b></sub>](https://github.com/vertex-app)<br /> | [<img src="https://img.pterclub.com/images/2023/09/29/p11a08.jpg" width="175px;"/><br /><sub><b>shmt86</b></sub>](https://pterclub.com/userdetails.php?id=751)<br /> | 
|:---------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
 








