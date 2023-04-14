# DataX

DataX 是阿里云 DataWorks数据集成 的开源版本，在阿里巴巴集团内被广泛使用的离线数据同步工具/平台。

项目传送门: https://github.com/alibaba/DataX

# DataX Web

DataX Web 是基于 DataX 开发的一个 Web 访问套件。



#### 使用方法

```bash
git clone https://github.com/gindowcloud/datax

cd datax

cp .env.example .env

docker-compose up -d
```



#### 访问地址

http://127.0.0.1:8000

用户: admin

密码: admin



#### 参数设置

除非有特定要求，通常无需进行参数配置，即可运行本程序，以下为常用配置参数：

##### 运行参数：
```bash
vi .env

DATAX_WEB_PORT=8000  # 前端（页面）运行容器端口
DATAX_API_PORT=8090  # 后端（接口）运行容器端口

PATH_DATA=~/.datax  # 数据存储路径，包括生成的脚本和日志
```

##### 接口参数（设置MYSQL数据库）：
```bash
vi backend/.env

DB_CONNECTION=mysql+pymysql  # 数据库驱动
DB_HOST=127.0.0.1  # 数据库地址
DB_PORT=3306  # 数据库端口
DB_USERNAME=root  # 数据库用户 
DB_PASSWORD=root  # 数据库密码
DB_DATABASE=datax  # 数据库名称

PYTHON=python  # Python 命令地址（非容器化运行时配置）
DATAX=/datax/bin/datax.py  # Datax 执行地址（非容器化运行时配置）
```

##### 页面参数：
```bash
vi frontend/.env

VITE_APP_NAME=数据管理平台  # 项目名称
VITE_BASE_URL=http://0.0.0.0:8090/api  # 页面调用的接口地址（重要，配置外网访问需要设置）
```

#### 版本更新
```bash
git pull

docker-compose build

docker-compose down

docker-compose up -d
```

#### 界面预览

用户登陆：
<img src="https://github.com/gindowcloud/assets/raw/master/datax/11.png" style="zoom: 50%;" />

任务管理：
<img src="https://github.com/gindowcloud/assets/raw/master/datax/21.png" style="zoom:50%;" />

<img src="https://github.com/gindowcloud/assets/raw/master/datax/22.png" style="zoom:50%;" />

<img src="https://github.com/gindowcloud/assets/raw/master/datax/23.png" style="zoom:50%;" />

计划管理：
<img src="https://github.com/gindowcloud/assets/raw/master/datax/31.png" style="zoom:50%;" />

<img src="https://github.com/gindowcloud/assets/raw/master/datax/32.png" style="zoom:50%;" />

连接管理：
<img src="https://github.com/gindowcloud/assets/raw/master/datax/41.png" style="zoom:50%;" />

用户管理：
<img src="https://github.com/gindowcloud/assets/raw/master/datax/51.png" style="zoom:50%;" />
