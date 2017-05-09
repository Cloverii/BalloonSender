# -*- coding: utf-8 -*-
# 1. what will happen when can't access the server
import re
import json
import urllib  
import urllib2
from Tkinter import *
import cookielib

def tryAccess():
    cookie = cookielib.MozillaCookieJar()
    if useCookies:
        cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)
    request = urllib2.Request('http://acm.cqu.edu.cn/contest_info.php?cid='+ conf['cinfo']['cid'])
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    result = opener.open(request).read()
    #print result
    pattern = re.compile(r'Contest Unavailable!')
    ret = re.match(pattern,result)
    return ret == None
    #return a corresponding MatchObject instance. Return None if the string does not match the pattern;

def login():
    filename = 'cookies.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode(conf['userinfo'])
    req = urllib2.Request(url = 'http://acm.cqu.edu.cn/ajax/login.php', data = postdata)
    res = opener.open(req)
    cookie.save(ignore_discard=True, ignore_expires=True)
    
    return res.read() == '{"code":0,"msg":"Success..."}'

def getStatus():
    cookie = cookielib.MozillaCookieJar()
    if useCookies:
        cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)
    data = urllib.urlencode(conf['cinfo'])
    request = urllib2.Request('http://acm.cqu.edu.cn/ajax/contest_status_data.php?' + data + 'randomid=0.8867441343120868&sEcho=5&iColumns=10&sColumns=&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8&mDataProp_9=9&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&sSearch_7=&bRegex_7=false&bSearchable_7=true&sSearch_8=&bRegex_8=false&bSearchable_8=true&sSearch_9=&bRegex_9=false&bSearchable_9=true&iSortCol_0=1&sSortDir_0=desc&iSortingCols=1&bSortable_0=false&bSortable_1=false&bSortable_2=false&bSortable_3=false&bSortable_4=false&bSortable_5=false&bSortable_6=false&bSortable_7=false&bSortable_8=false&bSortable_9=false&_=1494052227604')
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(request)
    result = response.read()
    if isNotBlank(result):
        return json.loads(result)
    else:
        return {}
    
def getNewAC():
    global lastRecord, total
    color = conf['color']
    lst = status['aaData']

    for item in lst:
        if((item[0], item[2])) in records:
            continue
        records.add((item[0], item[2]))
        res =[item[2], color[item[2]], item[0], item[1], item[8]]
        res[3] = int(res[3])
        if res[3] <= lastRecord:
            break;
        todoLst.append(res)
        
    total = int(status['iTotalDisplayRecords'])
    lastRecord = int(lst[0][1])


def existNewAC():
    #print(int(status['iTotalDisplayRecords']), total)
    return int(status['iTotalDisplayRecords']) != total
        
def frame(root, side):
    w = Frame(root)  
    w.pack(side = side, expand = YES, fill = BOTH)  
    return w  

def button(root, side, text, command = None):
    w = Button(root, text = text, command = command)  
    w.pack(side = side, expand = YES, fill = BOTH)  
    return w
    
def label(root, side, text, width): # name = "strname"
    w = Label(root, text = text, relief = "solid", width = width)
    w.pack(side = side, expand = YES, fill = BOTH)
    return w
    
def addToRmLst(i):
    rmLst.append(i)
    
def removeItems():
    newLst = list(set(rmLst))
    newLst.sort(reverse=True)
    for i in newLst:
        del(todoLst[i])
    del rmLst[:]

def isNotBlank (myStr):
    return bool(myStr and myStr.strip())

def main():
    global lastRecord, total, status, todoLst, rmLst, records, conf, useCookies
    lastRecord = -1
    total = 0
    todoLst = []
    rmLst = []
    records = set()
    flag = True
    useCookies = False
    with open('conf.json', 'r') as f:    
        conf = json.load(f)
    
    if 'userinfo' in conf:
        uinfo = conf['userinfo']
        if 'username' in uinfo and 'password' in uinfo:
            if isNotBlank(uinfo['username']) and isNotBlank(uinfo['password']):
                if login():
                    useCookies = True
    
    if useCookies and not tryAccess():
        print('Contest Unavailable! Check your config or permisson to the contest')
        return
    
    while(flag):
        root = Tk()
        removeItems()
        status = getStatus()
        #print(status)
        if status:
            if existNewAC():
                getNewAC()
        else:
            label(root, LEFT, 'ERROR! Please check your config.')
        
        
        root.title('Balloon Sender')
        root.attributes("-topmost", 1)
        root.geometry('+0+0') # 'axb+x+y'

        refresh = Button(root, text="Refresh", fg="red", command=root.destroy)
        refresh.pack(side="bottom")
        
        w = [3, 8, 20]
        for i in range(len(todoLst)):
                keyF = frame(root, TOP)
                label(keyF, LEFT, i, 3)
                for j in range(3):
                    txt = todoLst[i][j]
                    label(keyF, LEFT, txt, w[j])
                button(keyF, LEFT, 'Done', command = lambda i=i: addToRmLst(i))  
                # need to notify when a button is clicked twice

        root.mainloop()


if __name__ == '__main__':
    main()
