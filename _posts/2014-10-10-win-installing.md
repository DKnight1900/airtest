--- 
title: Win安装
layout: post
category: deployment
permalink: /deployment/win-installing.html
---

软件依赖 python2.7 32bit. 强调一遍<a style="color:red"> 32bit. not 64.</a>

从百度网盘下载安装依赖的软件包：

    网址：http://pan.baidu.com/s/1eQFyg4E
    密码: dt77

软件包中包含有：

    1. python-2.7.7-32bit
    2. pyparsing
    3. numpy
    4. dateutil
    5. matplotlib
    6. pillow
    7. pip
    8. setuptools
    9. opencv

上述安装完后，打开命令行，继续安装两个软件包

    easy_install -i http://mt.nie.netease.com:3141/simple/ androidviewclient    
    pip install -U -i http://mt.nie.netease.com:3141/simple/ airtest


最后下载adb.exe客户端 - [下载地址](ftp://mt.nie.netease.com/airtest-win-res/adb.zip),下好解压后放到PATH下, 软件[来源](http://adbshell.com/download/download-adb-for-windows.html)

adb介绍: <http://developer.android.com/tools/help/adb.html>

#### 其他说明
1. Android上已经支持特殊字符的输入，运行airtest时会自动安装一个输入法软件。感谢开源项目<https://github.com/senzhk/ADBKeyBoard> [软件地址](http://mt.nie.netease.com/files/airtest-android-res/adb-keyboard.apk)

2. airtest开发版安装方法，需要下载Git客户端。windows版git[点此下载](ftp://mt.nie.netease.com/airtest-win-res/Git-1.9.4-preview20140815.exe)

        pip install -U git+http://git.mt.nie.netease.com/hzsunshx/airtest.git



