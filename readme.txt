https://blog.csdn.net/qq_32437455/article/details/104815185


1.找到电影的index.m3u8文件url(这个文件中包含所有ts流文件名及顺序。后面需要通过该文件构造出所有的ts流文件下载，以及最后的合并顺序)，把index.m3u8的url地址写入到m3u8.txt文件中。


2.下载u3m8文件
3.读取u3m8文件，把里面ts小文件名放入一个列表中待用。
4.循环从步骤3中的列表中读取单个ts链接，并下载到指定的目录。
5.合并所有ts小文件为ts(或MP4)格式。
6.美滋滋的观赏。


对于下载下的ts流文件合并没有用代码实现，手工实现的，开始以为一个copy /b *.ts new.ts 就OK了，但是这种合并后的文件有各种小毛病，例如：卡屏、视频跳跃性播放等。
	所以这个时候需要安装一个 ffmpeg！安装完后创建一个xxx.bat脚本，脚本内容：
	>>>
	ffmpeg -allowed_extensions ALL -i index.m3u8 -c copy new.mp4
	del *.ts
	>>>
	-i :指定indexm3u8文件位置，因为需要这个文件中ts文件的顺序。
	-c copy: 新文件名字。

执行xxx.bat ->打开最终的new.mp4