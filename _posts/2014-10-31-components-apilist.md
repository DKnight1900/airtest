--- 
title: API接口列表
layout: post
category: components
permalink: /components/apilist.html
---
after installed successfully. you can import like `import airtest`

step1 connect device

    # get serialno by call: adb devices
    devno = os.getenv('AIRTEST_DEVNO') or 'xxxxx888882111' # <win_file_name | mac bundleid | android serialno>
    appname = os.getenv('AIRTEST_APPNAME') or 'com.netease.rz' # app name
    deviceType = 'android' # can be "windows" or "ios"

    # connect to your android devices
    # default value: device='android', monitor=True
    app = airtest.connect(devno, appname=appname, device=deviceType, monitor=True)

    app.monitor.start() # start monitor
    app.monitor.stop() # stop monitor
    app.globalSet(monitor_interval=1.0) # set monitor interval to 1s


#### takeSnapshot(filename) # filename show with extention (.jpg or .png)

    app.takeSnapshot('snapshot.png')


#### keepCapture()
图形查找时，使用上次的屏幕截图。可以用来提高脚本的运行效率。

#### releaseCapture()
关闭keepCapture

#### click(P, [seconds], duration=0.1) # click by image file

    长按的支持：
    eg: 点击2s  click((100, 200), duration=2.0)

    app.click(P)
    # P can be
    # - filename: 'start.png'
    # - position: (100, 200)
    # - percent: (0.1, 0.02)    # equal to (width*0.1, height*0.02)

    # click-timeout(only avaliable when P is string)
    # equals to app.click(app.find('start.png', 20.0))
    app.click('start.png', 20.0) # if start.png not found in 20s, Exception will raised.

#### find(image_file) # find a image position located in screen

    (x, y) = app.find(filename)


#### findall(self, imgfile, maxcnt=None, sort=None): # sort = <None|"x"|"y">

    findall('start.png', maxcnt=2)
    findall('start.png', maxcnt=2, sort='x') # sort ordered by x row

#### sleep(secs) # sleep for a while

    app.sleep(2.0)  # sleep 2.0s
    # same as time.sleep but can find sleep func call in log

#### log(tag_name, object)

    app.log('myTag', {'name': 'tt'})
    # log will be like {"timestamp": ..., "tag": "myTag", "data": {"name": "tt"}}

    # also support
    app.log('myTag', 'helloworld')

#### wait(...) # wait until image shows

    app.wait(filename, [seconds])
    # filename is the image name
    # seconds is the longest time waited.
    # @return position images find, or Raise RuntimeError
    # this is called find(..) to get images position


#### safeWait(filename, [seconds]) # like wait, but don't raise RuntimeError

    app.safeWait(filename) # return None if not found, else point


#### exists(...) # judge if image exists

    app.exists('apple.png')
    # @return (True|False)
    # just exactly call wait


#### shape() # get screen size(width and height)

    (w, h) = app.shape()
    # return width and height

#### drag(...) # drag one place to and onother place

    drag时间的支持, 如 drag 2s

    app.drag((x1, y1), (x2, y2), duration=2.0)

`app.drag(fromP, toP)` # fromP, toP: like click param, can be filename or position

    # example of drag from left to right
    (x1, y1), (x2, y2) = (w*0.2, h*0.5), (w*0.8, h*0.5)
    app.drag((x1,y1), (x2,y2))


#### type(...) # type text

    app.type('www.baidu.com\n') # type text and call keyevnet ENTER


#### keyevent(not recommemd to use now)

    # back and menu(only for android)
    app.keyevent('BACK')
    app.keyevent('MENU')


### airtest settting
Mobile phone has 4 directions: `UP,DOWN,LEFT,RIGHT`.
Change rotation through. more info view: <http://doc.mt.nie.netease.com/doku.php?id=airtest-screen-rotate>

    app.globalSet({'rotation': 'RIGHT'})


Change image recognize sensitivity

    # threshold range [0, 1)
    # the bigger the accurate. If set to 1, then app can't recognize anything
    app.globalSet({'threshold': 0.3}) 



