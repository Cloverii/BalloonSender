# -*- coding: utf-8 -*-
import json
import urllib  
import urllib2
from Tkinter import *
import cookielib

color = {'A':'red', 'B':'blue', 'C':'green', 'D':'purple'}

def getStatus():
    cid = '219'
    iDisplayStart = '0'
    iDisplayLength = '2000'
    sSearch_3 = 'Accepted'
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    req = urllib2.Request('http://acm.cqu.edu.cn/ajax/contest_status_data.php?cid=' + cid + '&randomid=0.8867441343120868&sEcho=5&iColumns=10&sColumns=&iDisplayStart=' + iDisplayStart + '&iDisplayLength=' + iDisplayLength + '&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8&mDataProp_9=9&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=' + sSearch_3 + '&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&sSearch_7=&bRegex_7=false&bSearchable_7=true&sSearch_8=&bRegex_8=false&bSearchable_8=true&sSearch_9=&bRegex_9=false&bSearchable_9=true&iSortCol_0=1&sSortDir_0=desc&iSortingCols=1&bSortable_0=false&bSortable_1=false&bSortable_2=false&bSortable_3=false&bSortable_4=false&bSortable_5=false&bSortable_6=false&bSortable_7=false&bSortable_8=false&bSortable_9=false&_=1494052227604')
    res = opener.open(req)
    
    return json.load(res)
    
def getNewAC():
    global lastRecord, total
    lst = status['aaData']
    #print status
    for item in lst:
        if((item[0], item[2])) in records:
            continue
        records.add((item[0], item[2]))
        res =[item[2].center(3, ' '), color[item[2]].center(8, ' '), item[0].center(20, ' '), item[1], item[8]]
        res[3] = int(res[3])
        #print(res[3], lastRecord)
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
    
def label(root, side, text):
    w = Label(root, text = text)
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

def main():
    global lastRecord, total, status, todoLst, rmLst, records
    lastRecord = -1
    total = 0
    todoLst = []
    rmLst = []
    records = set()
    flag = True
    
    while(flag):
        removeItems()
        status = getStatus()
        #print(existNewAC())
        if existNewAC():
            getNewAC()
        root = Tk()
        root.title('Balloon Sender')
        root.attributes("-topmost", 1)
        display = StringVar()
        refresh = Button(root, text="Refresh", fg="red", command=root.destroy)
        refresh.pack(side="bottom")
        for i in range(len(todoLst)):
                keyF = frame(root, TOP)
                label(keyF, LEFT, i)
                for j in range(3):
                    txt = todoLst[i][j]
                    label(keyF, LEFT, txt)
                button(keyF, LEFT, 'Done', command = lambda i=i: addToRmLst(i))  
                # two problems: 1. need to notify when a button is clicked twice
        root.mainloop()

if __name__ == '__main__':
    main()
