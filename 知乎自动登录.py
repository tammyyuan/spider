from http import cookiejar
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time
import requests
import sys
import os

session = requests.Session()
headers = {
"Referer": "https://www.zhihu.com/",
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
hosturl = "https://www.zhihu.com"

#加载cookies
session.cookies = cookiejar.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except :
    print("load cookies faild")

#获取_xsrf
def getxsrf():
    r = session.get("https://www.zhihu.com/",headers = headers)
    soup = BeautifulSoup(r.content,'html.parser')
    #print(soup.text)
    xsrf = soup.find("input",attrs={"name": "_xsrf"}).get("value")
    return xsrf

#获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url,headers = headers)
    #print(r.content)
    #soup = BeautifulSoup(r.content,'html5lib')
    #print(soup)
    with open("captcha.jpg","wb") as f:
        f.write(r.content)

    try:
        image = Image.open("captcha.jpg")
        #captcha  = image.tobytes().decode()
        #print(captcha)
        image.show()
        image.close()
    finally:
        captcha = input("验证码：")
    return captcha
    #return "9034"

#登录
def login(phone_num, password):
    loginurl = "https://www.zhihu.com/login/phone_num"
    data = {
        "_xsrf": getxsrf(),
        "password": password,
        #'captcha_type':"cn",
        "phone_num":phone_num,
        "captcha": get_captcha(),
        "remember_me":"true",
    }
    r = session.post(loginurl,data = data,headers = headers)
    print(r.text.json())
    session.cookies.save()
    for i in session.cookies :
        print(i)
#判断是否登录状态
def is_login():
    url = "https://www.zhihu.com/settings/profile"

    res = session.get(url,allow_redirects = False,headers = headers)
    login_code = res.status_code
    if int(login_code) == 200 :
        return True
    else:
        return False


def getcollection():

    colurl = "https://www.zhihu.com/collection/61913303"
    colres = session.get(colurl, headers = headers)
    colsoup = BeautifulSoup(colres.content,"lxml")
    for link in colsoup.find_all("div","zm-item-rich-text expandable js-collapse-body") :
        print(link["data-entry-url"])
        answerurl = hosturl + link["data-entry-url"]
        answerres = session.get(answerurl,headers = headers)
        ansswersoup = BeautifulSoup(answerres.content,"lxml")
        for data_original in ansswersoup.find_all("img","origin_image zh-lightbox-thumb"):
            # print(data_original)
            oriurl = data_original["data-original"]
            imgres = session.get(oriurl,headers = headers)
            print(oriurl)
            imgpath = savepath +"/" + os.path.split(oriurl)[1]
            destfile(oriurl)
            with open(imgpath, "wb") as f:
                f.write(imgres.content)

savepath = r"/Users/MaYingXin/Desktop/code/spider/zhihuzidongdenglu/轮子哥带我看世界by水见"
def destfile(path):
    if not os.path.isdir(savepath) :
        os.mkdir(savepath)
    pos = path.rindex("/")
    t = os.path.join(savepath, path[pos+1:])
    return t


if __name__ == '__main__' :
    phone_num = '17600400206'
    password = "931816682"

    if is_login():
        print("已经登录")
    else:
        login(phone_num, password)

    getcollection()
    print("finished.")