# -*- coding: utf-8 -*-
# test:
# 1. normal public contest (scheduled or running or ended)
# 2. private contest (with usename & password or with one of them or with wrong password)
# 3. network error
# 4. ...
import re
import json
import urllib  
import urllib2
from Tkinter import *
import cookielib

class Connector:
    cookie = cookielib.CookieJar()
    
    def login(self, userinfo):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Connector.cookie))
        postdata = urllib.urlencode(userinfo)
        req = urllib2.Request(url = 'http://acm.cqu.edu.cn/ajax/login.php', data = postdata)
        res = opener.open(req)
        strr = res.read()
        return res.read() == '{"code":0,"msg":"Success..."}'

    def permission(self, cid): # Return false if current user doesn't have enough permission
        request = urllib2.Request('http://acm.cqu.edu.cn/contest_info.php?cid='+ cid)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Connector.cookie))
        result = opener.open(request).read()
        #print result
        pattern = re.compile(r'Contest Unavailable!')
        ret = re.match(pattern,result)
        return ret == None
        #return a corresponding MatchObject instance. Return None if the string does not match the pattern;

    def getStatus(self, cinfo):
        data = urllib.urlencode(cinfo)
        request = urllib2.Request('http://acm.cqu.edu.cn/ajax/contest_status_data.php?' + data)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Connector.cookie))
        response = opener.open(request)
        result = response.read()
        if isNotBlank(result):
            return json.loads(result)
        else:
            return {}

class Controller:
    def __init__(self):
        self.totalNum = 0
        self.lastRecord = -1
        self.todoLst = []
        self.rmLst = []
        self.records = set()
        self.cn = Connector()
        self.login()

    def login(self):
        with open('conf.json', 'r') as f:    
            self.conf = json.load(f)
        
        if 'userinfo' in self.conf:
            uinfo = self.conf['userinfo']
            if 'username' in uinfo and 'password' in uinfo:
                if isNotBlank(uinfo['username']) and isNotBlank(uinfo['password']):
                    self.cn.login(uinfo)
                        
    def access(self):    
        return self.cn.permission(self.conf['cinfo']['cid'])
            
    def existNewAC(self):
        return int(self.status['iTotalDisplayRecords']) != self.totalNum

    def getNewAC(self, color):
        lst = self.status['aaData']

        for item in lst:
            if((item[0], item[2])) in self.records:
                continue
            self.records.add((item[0], item[2]))
            cl = "notset"
            if item[2] in color:
                cl = color[item[2]]
            res =[item[2], cl, item[0], item[1], item[8]]
            res[3] = int(res[3])
            if res[3] <= self.lastRecord:
                break;
            self.todoLst.append(res)
            
        self.totalNum = int(self.status['iTotalDisplayRecords'])
        self.lastRecord = int(lst[0][1])
     
    def refresh(self):
        self.removeItems()
        self.status = self.cn.getStatus(self.conf['cinfo'])
        #print(self.status)
        if self.status == {}:
            self.login() # try login if can't access (you can change conf without restarting the program)
            self.status = self.cn.getStatus(self.conf['cinfo'])
        if self.status != {}:            
            if self.existNewAC():
                self.getNewAC(self.conf['color'])
            return True
        return False
    
    def addToRmLst(self, i):
        self.rmLst.append(i)
        
    def removeItems(self):
        newLst = list(set(self.rmLst))
        newLst.sort(reverse=True)
        for i in newLst:
            del(self.todoLst[i])
        del self.rmLst[:]
    
    def getList(self):
        return self.todoLst
            
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

def isNotBlank (myStr):
    return bool(myStr and myStr.strip())

def main():
    ctl = Controller()
    if not ctl.access():
        print('Contest Unavailable! Check your config or permisson to the contest')
    flag = True
    #lst = []
    while(flag):
        root = Tk()
        
        lst = []
        if ctl.refresh():
            lst = ctl.getList()
        else:
            label(root, LEFT, 'ERROR! Please check your user config.', 50)
        
        
        root.title('Balloon Sender')
        root.attributes("-topmost", 1)
        root.geometry('+0+0') # 'axb+x+y'

        refresh = Button(root, text="Refresh", fg="red", command=root.destroy)
        refresh.pack(side="bottom")
        
        w = [3, 8, 20]
        for i in range(len(lst)):
                keyF = frame(root, TOP)
                label(keyF, LEFT, i + 1, 3)
                for j in range(3):
                    txt = lst[i][j]
                    label(keyF, LEFT, txt, w[j])
                button(keyF, LEFT, 'Done', command = lambda i=i: ctl.addToRmLst(i))
                # need to notify when a button is clicked twice

        root.mainloop()


if __name__ == '__main__':
    main()
