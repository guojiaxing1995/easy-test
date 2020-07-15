<h1 align="center">Easy-Test</h1>
<h4 align="center">接口自动化测试平台</h3>

<p align="center">
  <a href="https://www.python.org/" rel="nofollow"><img src="https://img.shields.io/badge/python-%3D%3D3.6-blue.svg" alt="python version" data-canonical-src="https://img.shields.io/badge/python-%3D%3D3.6-blue.svg" style="max-width:100%;"></a>
  <a href="http://flask.pocoo.org/docs/1.0/" rel="nofollow">
  <img src="https://img.shields.io/badge/flask-%3D%3D1.0.2-yellow.svg" alt="flask version" data-canonical-src="https://img.shields.io/badge/flask-%3D%3D1.0.2-yellow.svg" style="max-width:100%;"></a>
  <a href="https://nodejs.org/en/"><img src="https://img.shields.io/badge/node-%3D%3D10.16.0-green" alt="node version" data-canonical-src="https://img.shields.io/badge/vue-%3D%3D2.9.6-green.svg" style="max-width:100%;"></a>
</p>


### 项目介绍
<font face="楷体" color=gray>接口自动化测试平台现在已经实现了多接口批量测试、用例管理、测试集内用例依赖关系处理、分布式异步测试执行、测试集灵活配置、测试结果多维度查看、定时任务、用例调试、mock数据管理和测试结果邮件通知等功能。</font>

<font face="楷体" color=gray>平台技术栈为 vue + python falsk 前后端分离实现，数据库使用的是mysql和mongodb，异步任务用到了rabbitmq。</font>

<font face="楷体" color=gray>源码地址：[https://github.com/guojiaxing1995/easy-test](https://github.com/guojiaxing1995/easy-test)</font>

<font face="楷体" color=gray>在线接口文档：[https://www.showdoc.cc/easyTest](https://www.showdoc.cc/easyTest)</font>

<font face="楷体" color=gray>使用文档：[https://blog.csdn.net/qq_36450484/article/details/107332571](https://blog.csdn.net/qq_36450484/article/details/107332571)</font>

### 部分模块展示

![测试总览](https://img-blog.csdnimg.cn/20200714191705596.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70#pic_center)

![测试执行](https://img-blog.csdnimg.cn/20200714224113706.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70#pic_center)

![测试结果详情](https://img-blog.csdnimg.cn/20200715085628153.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70#pic_center)

![mock管理](https://img-blog.csdnimg.cn/20200715173300210.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70#pic_center)
### 系统架构
![系统架构图](https://img-blog.csdnimg.cn/20200714182757692.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70#pic_center)
浏览器请求从web前端到api服务后端，包括http请求和socketio请求。api后端服务访问mysql和mongodb数据库对数据增删改查，同时其也作为生产者将任务数据加入到rabbitmq队列中。worker作为消费者连接队列后消费队列数据执行任务，执行过程中操作数据库并请求api服务后端通过websocket连接向前端广播数据。


### 项目本地调试
**easy-test-vue（前端）**

   在 easy-test-vue 目录下执行

``` javascript
npm install
npm run serve
```
指向2个后端的接口地址请查看main.js 和 Container.vue 文件中的注释。部署和本地运行这里不同。

**easy-test-flask（后端）**

   在 easy-test-flask 目录下执行
   后端服务启动

``` shell
pip install -r requirements.txt
python starter.py
```
worker 启动
``` shell
celery -A starter.celery worker -l info --pool=solo
```



### 平台docker部署
平台的所有服务、中间件和数据库都使用docker进行部署。
前端打包命令`npm run build`。前端vue项目使用nginx部署，`default.conf`配置文件在vue项目目录下，我配置了域名，部署时可以根据自己情况修改。
后端flask配置文件路径为`\app\config`，只需要修改静态服务地址`SITE_DOMAIN`（此处我在nginx配置中做了转发，如果不需要则删除nginx配置文件中assets相关配置）。
worker可以根据自己的资源启动多个，修改compose文件即可。
flask工程目录下有api服务镜像构建文件`Dockerfile-api`和worker服务镜像构建文件`Dockerfile-worker`，vue工程目录下有前端服务镜像构建文件`Dockerfile`,工程目录下有`docker-compose.yaml`文件,该文件只需要酌情修改端口映射。镜像无需手动执行构建命令构建，服务启动会自动构建。
<br>
**服务启动**

```shell
docker-compose up -d
```
**服务停止**

```shell
docker-compose down
```
![服务部署](https://img-blog.csdnimg.cn/20200715190204815.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70#pic_center)
上图红框标注处为部署成功后所有的服务。

<br>
<span">关于系统有任何问题请联系： 302802003@qq.com</span>
