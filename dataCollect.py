import re
import requests
from bs4 import BeautifulSoup


news=[]
def getText(url):#获取网页text及新闻内容和发布时间
    headers={
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        'Cookie': 'SINAGLOBAL=5544090271390.932.1610187708338; SUB=_2A25y_f4SDeThGeFP7lQQ9S7JzDmIHXVuAYJarDV8PUJbkNANLW3ikW1NQQ46xjFBP3Gsy9o4X4EO507Zo3CyHX7D; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW1Kd_YQkpJQ-Y_2LXJX80J5NHD95QNeK-ceK-7SKMfWs4DqcjDi--Xi-iWiK.pi--ci-2Ei-2ci--fi-2Xi-24i--NiKyFi-iheK20e0nt; wvr=6; wb_view_log_7156150575=1536*8641.25; _s_tentry=www.baidu.com; Apache=851030178356.7264.1610941239675; ULV=1610941239714:4:4:3:851030178356.7264.1610941239675:1610897251135; UOR=,,www.baidu.com; webim_unReadCount=%7B%22time%22%3A1610971312491%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A41%2C%22msgbox%22%3A0%7D' #这里要自己用f12获取自己登陆的微博cookie
    }
    try:
        r=requests.get(url,headers = headers)
        r.raise_for_status()
        r.encoding="utf-8"
        content=r.text.split('】')[1]
        content=content.split('</span>')[0]


        time=r.text.split("是否进行翻译")[1]
        time=time.split("举报")[0]
        time=time.split('<span class="ct">')[1]
        time=time.split('    </span>')[0]
        news.append({"内容":content,"时间":time})

        return r.text

    except:
        return ""

def getComments(xml):
    comments=[]
    div0=BeautifulSoup(xml,"xml").find_all("div",attrs={"class" : "c"})
    div=[]
    for i in range(len(div0)):
        if  'id="C' in str(div0[i]):
            div.append(div0[i])
    for i in range(len(div)):
        try:
            tmpComment=re.compile(r'<span class="ctt.*?</span>').search(str(div[i]))[0]
            if "回复" in tmpComment:
                comment=re.compile(r'</a>.*</span>').search(str(tmpComment))[0].replace("</a>:","").replace("</span>","")
            else:
                comment=tmpComment.replace('<span class="ctt">','').replace('</span>','')
            if "</a>" in comment:
                tmp=re.compile(r'<a.*?/a>').search(str(comment))
                for m in range(len(tmp)):
                    comment=comment.replace(tmp[m],"")

            if comment:
                comments.append(comment)
        except:
            continue
    return comments

def run():#根据url获取新闻内容/发布时间/评论
    urlList=[]
    with open('urls','r',encoding='UTF-8') as f:
        for line in f:
            urlList.append(line)

    urlNum,newsNum=0,0
    while urlNum<len(urlList):
        url=urlList[urlNum]+'&page={}'.format(1)
        text=getText(url)
        comments=getComments(text)

        news[urlNum]['评论']=[]
        i=0
        while i<len(comments) and i<10:
            news[urlNum]['评论'].append(comments[i])
            i+=1

        if len(news[urlNum]["评论"]) != 0:
            with open('newsData.txt','a',encoding="UTF-8") as f:
                f.write(str(newsNum+1)+'\n')
                newsNum+=1
                f.write("新闻内容:  "+news[urlNum]["内容"]+'\n')
                f.write("发布时间:  "+news[urlNum]["时间"]+'\n')
                f.write("评论:"+'\n')
                commentNum=1
                for com in news[urlNum]["评论"]:
                    f.write("          "+str(commentNum)+'.'+str(com)+'\n')
                    commentNum=commentNum+1
                f.write('\n')
                print("已完成"+str(urlNum + 1)+"条")

        urlNum+=1
