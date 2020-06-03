# Duo Shou Store

基于python(version >= 3.7)和Tornado 6.x的SAAS购物平台

## 安装

### 1. 使用Docker镜像运行环境
我们提供了一个运行环境的Docker镜像，可以非常方便的启动服务
#### 获取镜像
```shell script
docker pull onlyfu/ddsp:latest
```
#### 启动镜像
```shell script
docker run --name python -p 9000:9000 -t docker.io/onlyfu/ddsp:latst
```

### 2. 自行安装信赖包

- tornado>=5.0.2
- tornado-redis
- aioredis
- tormysql
- urllib3
- tornado-smtp

## 使用
### Step 1. 修改配置文件
配置文件在项目根目录conf文件夹里，根据配置内容填写相关数据项即可

**建议将配置文件放到项目外，启动时使用-c参数来指定配置文件目录**

### Step 2. 启动服务
```shell script
python3 index.py -h 0.0.0.0 -p 端口号 -c '配置文件目录路径'
```
> -h: host
>
> -p: port
>
>-c: 配置文件目录，如果不传直接使用项目根目录下conf文件夹

## 二次开发

## 功能介绍

### 特点
1. 支持多店铺
2. 支持平台商城
3. 支持跨店购买
4. 支持供货/分销
