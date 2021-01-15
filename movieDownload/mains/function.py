# -*- coding:utf-8 -*-

import requests
import mains.getConfig as conf
import logging

'''设置日志格式'''
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='../log/log.log',
                    filemode='w'
                    )

'''从指定的m3u8.txt中获取所有url（m3u8）链接'''


def getM3u8List(m3u8FilePath):
    '''
    :param m3u8FilePath: m3u8.txt文件的路径，即存放url的文件路径
    :return: 返回一个m3u8链接的列表
    '''
    with open(m3u8FilePath, "r", encoding="utf-8") as f:
        m3u8List = f.readlines()
    return m3u8List


'''下载index.m3u8文件'''


def downladM3u8File(urlName, savePath):
    '''
    :param urlName: 需要下载的m3u8文url件链接 。
    :param savePath: 保存路径。
    :return: index.m3u8文件中ts链接的列表
    '''
    tsList = []
    loop = 0
    # 把下载的文件内容存入指定文件夹
    requesFileContent = requests.get(urlName, timeout=int(conf.timeOut)).content
    try:
        with open(savePath, "wb") as fo:
            fo.write(requesFileContent)
            logging.debug(urlName + " 下载成功!")
            print(urlName + " 下载成功!")

    # 如果下载失败，打印错误重新下载（重复5次）
    except Exception as e:
        print(e)
        if loop < 5:
            downladM3u8File(urlName, savePath)
        else:
            logging.debug(urlName + "未下载成功！")
            print(urlName + "未下载成功！")
        loop += 1

    # 打开下载的index.m3u8文件，获取ts流链接地址
    with open(savePath, "r", encoding="utf-8") as f:
        u3m8FileList = f.readlines()
        for i in u3m8FileList:
            if i[0] != "#":
                i = i[:-1]
                tsList.append(i)
    return tsList


'''下载ts文件'''


def downloadTsFile(urlName, savePath):
    '''
    :param urlName: 需下载的ts链接
    :param savePath: 保存路径
    :return:
    '''
    try:
        requestsContent = requests.get(urlName, timeout=int(conf.timeOut)).content
        with open(savePath, "wb") as f:
            f.write(requestsContent)
            print(urlName + " 下载成功！")
    except Exception as e:
        print(e)
        # downloadTsFile(urlName, savePath)
        # print(urlName + "下载失败！")
