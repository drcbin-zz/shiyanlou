import os
import threading 
import re
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from urllib.request import urlopen
from selenium import webdriver

# 设置基本变量
browserPath = '/opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
# browserPath = '/usr/bin/firefox'
homePage = 'https://mm.taobao.com/search_tstar_model.htm?'
outputDir = 'photo/'
parser = 'html5lib'
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}


def main():
    # 模拟浏览器抓取
    diver = webdriver.PhantomJS(executable_path=browserPath)
    # diver = webdriver.Firefox(executable_path=browserPath)
    diver.get(homePage)
    print('Send request')

    # 解析出girllist, text函数会忽略html代码,直接获取text文本， 包含了身高体重姓名地址
    girlList = diver.find_element_by_id('J_GirlsList').text.split('\n')
    print('Parser girlList')

    # 解析出封面图片src属性
    imageUrl = re.findall('\/\/gtd\.alicdn\.com\/sns_logo.*\.jpg', diver.page_source)
    print('Parser images.src')

    # 解析成bs对象
    bsObj = BeautifulSoup(diver.page_source, parser)
    print('get bsObj')

    # 定位到主页链接元素
    girlsUrl = bsObj.find_all('a', {'href': re.compile("\/\/.*\.htm\?(userId=)\d*")})
    print('Find home url element')





    # 每隔三个取一次
    girlNL = girlList[::3]

    # 从1开始,每隔3个取一次
    girlsHW = girlList[1::3]

    # 通过主页链接元素,获取到主页链接
    girlsHURL = [('http:' + i['href']) for i in girlsUrl]

    # 根据解析得到的src属性,生成url地址
    girlsPhotoUrl = [('https:' + i) for i in imageUrl]

    # 打包成可迭代对象
    girlsInfo = zip(girlNL, girlsHW, girlsHURL, girlsPhotoUrl) # zip打包， 可能会出错, 如果长度不一样的话

    p = Pool(40)

    for girlNL, girlsHW, girlsHURL, girlCover in girlsInfo:
        # 迭代所有model
        print("[*]Girl :", girlNL, girlsHW)

        # 为model创建文件夹
        mkdir(outputDir + girlNL)
        print("     [*]Saving...")

        # 获取封面图片并保存
        data = urlopen(girlCover).read()
        with open(outputDir + girlNL + '/cover.jpg', 'wb') as f:
            f.write(data)
        print("     [+]Loading Couver...")

        # 抓取该Model主页的所有图片
        p.apply_async(getImgs, args=(girlsHURL, outputDir + girlNL))

    # 关闭进程池
    p.close()
    p.join()
    print('[*]Done')
    # 关闭浏览器

    diver.close()



# 创建文件夹
def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("     [*]新建了文件夹", path)
    else:
        print("     [+]文件夹", path, '已存在')




def getImgs(url, path):
    # 打开链接
    diver = webdriver.PhantomJS(executable_path=browserPath)
    print('     [*]try open:', url)
    diver.get(url)
    print("     [*]opening...")

    # 解析成bs对象
    bsObj = BeautifulSoup(diver.page_source, parser)

    # 定位到到所有的img元素
    imgs = bsObj.find_all('img', {'src': re.compile('.*\.jpg')})
    print('     [-]获取到', len(imgs), '张图片')

    # a = 'abc'
    # enumerate(a) // [(0,a), (1,b), (2,c)]
    for i, img in enumerate(imgs[1:]):   # imgs[0]为头像,分辨率低, 直接过滤
        if i > 20:
            break
        try:
            # 构建image url
            html = urlopen('https:' + img['src'])
            print('     [*]Get image:', img['src'])

            # 获取image并写入文件夹
            data = html.read()
            fileName = '{}/{}.jpg'.format(path, i + 1)
            print('     [+]Loading...', fileName)
            with open(fileName, 'wb') as f:
                f.write(data)
        except Exception as e:
            print('     [!]Adress Error!')
    diver.close()


if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    main()
