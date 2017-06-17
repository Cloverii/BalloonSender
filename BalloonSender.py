#!/usr/bin/python2
# -*- coding: utf-8 -*-
# test cases:
# 1. normal public contest (scheduled or running or ended)
# 2. private contest (with usename || password, maybe wrong password)
# 3. network error, including timeout or 502
# 4. ...
import re
import json
import urllib
import urllib2
import Tkinter as tk
import cookielib


class Connector(object):
    cookie = cookielib.CookieJar()

    def login(self, userinfo):  # return true if success login
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Connector.cookie))
        postdata = urllib.urlencode(userinfo)
        req = urllib2.Request(
            url='http://acm.cqu.edu.cn/ajax/login.php',
            data=postdata
        )
        res = opener.open(req)
        # strr = res.read()
        return res.read() == '{"code":0,"msg":"Success..."}'

    # Return false if current user doesn't have enough permission
    def permission(self, cid):
        req = urllib2.Request('http://acm.cqu.edu.cn/contest_info.php?cid=' + cid)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Connector.cookie))
        result = opener.open(req).read()
        # print result
        pattern = re.compile(r'Contest Unavailable!')
        ret = re.match(pattern, result)
        # return a corresponding MatchObject instance.
        # Return None if the string does not match the pattern;
        return ret is None

    # need to add a timer, and return different msg for timeout, no ac and ...
    def get_status(self, cinfo):
        data = urllib.urlencode(cinfo)
        req = urllib2.Request('http://acm.cqu.edu.cn/ajax/contest_status_data.php?' + data)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(Connector.cookie))
        response = opener.open(req)
        result = response.read()
        if isnot_blank(result):
            return json.loads(result)
        else:
            return {}


class Controller(object):
    def __init__(self):
        self.total_num = 0
        self.last_record = -1
        self.todo_lst = []
        self.rm_lst = []
        self.archive_records = []
        self.records = set()
        self.cn = Connector()
        self.login()
        with open('archive.json', 'r') as f:
            try:
                # print(f.read())
                self.archive_records = json.load(f)
                print(self.archive_records)
            except ValueError, e:
                print('%s when reading "archive.json"' % (str(e)))

    def login(self):
        with open('conf.json', 'r') as f:
            self.conf = json.load(f)

        if 'userinfo' in self.conf:
            uinfo = self.conf['userinfo']
            if 'username' in uinfo and 'password' in uinfo:
                if isnot_blank(uinfo['username']) and isnot_blank(uinfo['password']):
                    self.cn.login(uinfo)

    def access(self):
        return self.cn.permission(self.conf['cinfo']['cid'])

    def exist_new_ac(self):
        return int(self.status['iTotalDisplayRecords']) != self.total_num

    def get_new_ac(self, color):
        lst = self.status['aaData']

        for item in lst:
            if item[3] != 'Accepted':  # why!!!!!!!!!!!!!!!!!!
                continue
            cur = (item[0].decode('utf-8'), item[2].decode('utf-8'))
            # plainstring1 = unicode(utf8string, "utf-8")
            if cur in self.records or cur in self.archive_records:
                # what is in records? what is in archive_records?
                continue
            self.records.add(cur)
            cl = "notset"
            if item[2] in color:
                cl = color[item[2]]
            res = [item[2], cl, item[0], item[1], item[8]]
            res[3] = int(res[3])
            if res[3] <= self.last_record:
                break
            self.todo_lst.append(res)

        self.total_num = int(self.status['iTotalDisplayRecords'])
        self.last_record = int(lst[0][1])

    def refresh(self):
        self.remove_items()
        self.status = self.cn.get_status(self.conf['cinfo'])
        # print(self.status)
        if self.status == {}:
            self.login()
            # try login if can't access
            # (you can change conf without restarting the program)
            self.status = self.cn.get_status(self.conf['cinfo'])
        if self.status != {}:
            if self.exist_new_ac():
                self.get_new_ac(self.conf['color'])
            return True
        return False

    def add_to_rm_lst(self, i):
        self.rm_lst.append(i)

    def remove_items(self):
        newLst = list(set(self.rm_lst))
        newLst.sort(reverse=True)

        with open('archive.json', 'r') as f:
            try:
                json.load(f)
            except ValueError, e:
                print('%s when reading "archive.json"' % (str(e)))
        with open('archive.json', 'w') as f:
            for i in newLst:
                cur = self.todo_lst[i]
                self.archive_records.append([cur[0], cur[2]])
            # json.dump(archive_records, f)
            # print(json.dumps(self.archive_records))
            json.dump(self.archive_records, f)

        for i in newLst:
            del(self.todo_lst[i])
        del self.rm_lst[:]

    def get_list(self):
        return self.todo_lst


def add_frame(root, side):
    w = tk.Frame(root)
    w.pack(side=side, expand=tk.YES, fill=tk.BOTH)
    return w

def add_button(root, side, text, command=None):
    w = tk.Button(root, text=text, command=command)
    w.pack(side=side, expand=tk.YES, fill=tk.BOTH)
    return w

def add_label(root, side, text, width):  # name = "strname"
    w = tk.Label(root, text=text, relief="solid", width=width)
    w.pack(side=side, expand=tk.YES, fill=tk.BOTH)
    return w

def isnot_blank(myStr):
    return bool(myStr and myStr.strip())

def main():
    ctl = Controller()
    if not ctl.access():
        print('Contest Unavailable! '
              'Check your config or permisson to the contest')
    flag = True
    # lst = []
    while(flag):
        root = tk.Tk()

        lst = []
        if ctl.refresh():
            lst = ctl.get_list()
        else:
            add_label(root, LEFT, 'ERROR! Please check your user config.', 50)

        if len(lst) == 0:
            add_label(root, LEFT, 'No unchecked AC records now~', 50)

        root.title('Balloon Sender')
        root.attributes("-topmost", 1)
        root.geometry('+0+0')  # 'axb+x+y'

        refresh = tk.Button(root, text="Refresh", fg="red", command=root.destroy)
        refresh.pack(side="bottom")

        w = [3, 8, 20]
        for i in range(len(lst)):
            keyF = add_frame(root, tk.TOP)
            add_label(keyF, tk.LEFT, i + 1, 3)
            for j in range(3):
                txt = lst[i][j]
                add_label(keyF, tk.LEFT, txt, w[j])
            add_label(keyF, tk.LEFT, lst[i][4], 25)
            add_button(
                keyF, tk.LEFT, 'Done',
                command=lambda i=i: ctl.add_to_rm_lst(i)
            )
            # need to notify when a button is clicked twice

        root.mainloop()


if __name__ == '__main__':
    main()
