Change Log
=================

### 2014/07/17
1. 增加start,stop,clear函数
1. globalSet增加mem和cpu监控周期调整。globalSet({'monitor_interval': 5})

### 2014/07/21
1. 增加airtest自测代码
2. 修正ios中的屏幕旋转问题
3. 增加关于屏幕设置的文档

### 2014/07/31
1. dev.getMem接口调整，原来返回PSS值，现在返回{'PSS':pss, 'VSS':vss, 'RSS':rss}
2. 新增airtest的图形界面，方面快速的截图和写代码
3. 图像文件名支持unicode中文，支持在多个图片文件夹里自动搜索
4. 增加globalGet函数

