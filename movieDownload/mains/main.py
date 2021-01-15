# coding=utf-8
"""
下载流式  m3u8  ts电影
"""

import os
import traceback
import mains.getConfig as conf
import mains.function as fun
from multiprocessing import Pool

if __name__ == "__main__":
    try:
        fun.logging.debug("【需要下载的电影url文件目录】:" + conf.m3u8FilePath)
        fun.logging.debug("【下载文件存储的根目录】:" + conf.filePath)
        print("【需要下载的电影url文件目录】:" + conf.m3u8FilePath)
        print("【下载文件存储的根目录】:" + conf.filePath)

        m3u8FilePath = conf.m3u8FilePath  # m3u8.txt文件的路径,从配置文件获取
        filePath = conf.filePath  # 下载的文件存储根目录，从配置文件获取
        urlList = fun.getM3u8List(m3u8FilePath)  # 获取m3u8.txt文件中的需要下载的url链接数量并放入列表。
        fun.logging.debug("【需要下载的url数量】:" + str(len(urlList)))
        print("【需要下载的url数量】:" + str(len(urlList)))
        newDir = 0  # 定义一个变量newDir,每个url下载的ts流文件放在单独的一个文件夹中，文件夹名从0开始。

        for i in urlList:  # 循环取urlList的url
            i = i.replace('\n', '')  # 取出的url链接末尾会有一个换行符，去掉。
            needDir = filePath + str(newDir)  # 构造新目录存放下载的ts文件，文件夹不存在的时候创建。
            if not os.path.exists(needDir):
                os.mkdir(needDir)

            m3u8SavePath = needDir + "\\" + conf.postFix  # 构造存储m3u8文件数据的文件名，。
            fun.logging.debug("【正在下载的是】:" + i + conf.postFix)
            print("【正在下载的是】:" + i + conf.postFix)
            tsList = fun.downladM3u8File(i + conf.postFix, m3u8SavePath)  # 下载并遍历并获取m3u8中的ts。

            # 下载key文件，有的网站ts流文件是加密的，需要下载下来key.key文件便于最后文件的合并。
            with open(conf.filePath + str(newDir) + "\\" + conf.postFix, 'r') as m3u8Index:
                key = m3u8Index.readlines()[4]
                if key[-5:-2] == "key":
                    fun.logging.debug("【正在下载的是】:" + i + "key.key")
                    print("【正在下载的是】:" + i + "key.key")
                    fun.downloadTsFile(i + "key.key", conf.filePath + str(newDir) + "\\" + "key.key")
            fun.logging.debug("【ts文件数量共】:" + str(len(tsList)) + "\n【开始下载ts文件】")
            print("【ts文件数量共】:" + str(len(tsList)) + "\n【开始下载ts文件】")
            newDir = newDir + 1

            # 下载ts文件
            tsIsOver = True
            while tsIsOver:
                pool = Pool(10)  # 定义线程数量pool，利用多线程下载提高效率。
                for j in tsList:
                    tsSavePath = needDir + "\\" + j  # 下载的ts文件存放路径。
                    if os.path.exists(tsSavePath):
                        pass
                    else:
                        pool.apply_async(fun.downloadTsFile, (i + j, tsSavePath))
                pool.close()
                pool.join()

                # 判断ts文件是否下载完毕，没下载完就继续下载。
                lostList = []
                for ts in tsList:
                    tsSavePath_bak = needDir + "\\" + ts
                    print("正在测试中......", tsSavePath_bak)
                    if not os.path.exists(tsSavePath_bak):
                        lostList.append(ts)
                if len(lostList) > 0:
                    tsIsOver = True
                    fun.logging.debug("ts文件没有下载完，继续下载！")
                    print("ts文件没有下载完，继续下载！")
                else:
                    tsIsOver = False
                    fun.logging.debug("ts文件已经下载完！")
                    print("ts文件已经下载完！")

    except Exception as ex:
        fun.logging.error(ex)
        print(ex)
        fun.logging.error(traceback.print_exc())
        # print("【错误位置】:"+traceback.print_exc())
