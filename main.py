#!/usr/bin/python3
#coding=utf-8
import itchat, time, os
from itchat.content import *
g_u_s=['a_b_1','a_c_1']
def update_gus(group,user,string):
    global g_u_s
    j=0
    for ex in g_u_s:
        if group+"_"+user+"_" in ex:
            g_u_s.pop(j)
        j=j+1
    g_u_s.append(group+"_"+user+"_"+string)
    print(g_u_s)
def get_gus(group,user):
    global g_u_s
    j=0
    for ex in g_u_s:
        if group+"_"+user+"_" in ex:
            return g_u_s[j].split('_')[2]
        j=j+1
def db2html(grpname, dirname):
    if not os.path.exists(dirname):
        os.system("mkdir "+dirname)
        print("had commited mkdir "+dirname)
    wi=300
    gn='ls '+dirname+"/"+grpname+'*.* -t'
    a=os.popen(gn).read().splitlines()
    fn=dirname+"/"+dirname+".html"
    la="ee"
    with open(fn,"w") as fo:
        fo.write("<meta http-equiv=\"content-type\" content=\"text/html;charset=utf8\"><table border = \"1\"><tr>")
        for b in a:
            b1=b.split("/")
            b2=b1[1]
            r=b2.split("_")
            if(len(r)>3):
              if(la!=r[2]):
                  fo.write("</tr><tr><td>"+r[2]+":</td>")
                  la=r[2]
                  wi=300
              else:
                  wi=100
              fo.write("<td><a href = \""+b2+"\" target = \"_blank\">")
              if(b2[-3:]=="mp4"):
                  fo.write("<video controls=\"controls\" autoplay=\"false\" width = \""+str(wi)+"\"><source src=\"./"+b2+"\" >浏览器不支持</video>")
              else:
                  fo.write("<img src=\"./"+b2+"\" width = \""+str(wi)+"\"/>")
              fo.write("</a><BR>"+r[4]+"</td>")
        fo.write("</tr><table>")

@itchat.msg_register([PICTURE, VIDEO], isGroupChat = True)
def groupchat_reply(msg):
    n_name='nikname'
    sender='adm'
    obj_name=' '
    if not msg['ActualNickName']:
        sender='adm'
    else:
        sender=msg['ActualNickName']
    try:
        obj_name=str(get_gus(msg['User']['NickName'],sender))
    except TypeError:
        obj_name="未命名"

    try:
        n_name=msg['User']['NickName']
    except KeyError:
        n_name="nikname"

#    dirname = msg['User']['NickName']+"_"+time.strftime("%Y%m%d")
    dirname = n_name+"_"+time.strftime("%Y%m%d")
    if not os.path.exists(dirname):
      os.system("mkdir "+dirname)
#    wf=".\\"+dirname+"\\"+msg['User']['NickName']+"_"+time.strftime("%Y%m%d")+"_"+sender+"_"+time.strftime("%H%M%S")+"_"+obj_name+"."+msg['FileName'].split(".")[1]
    wf="./"+dirname+"/"+n_name+"_"+time.strftime("%Y%m%d")+"_"+sender+"_"+time.strftime("%H%M%S")+"_"+obj_name+"."+msg['FileName'].split(".")[1]
    msg['Text'](wf)
    print(wf)
#    db2html(msg['User']['NickName'],dirname)
    db2html(n_name,dirname)
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def update_key_words(msg):
    sender='adm'
    if not msg['ActualNickName']:
        sender='adm'
    else:
        sender=msg['ActualNickName']
    update_gus(msg['User']['NickName'],sender,msg['Content'])

itchat.auto_login(hotReload=True,enableCmdQR=2)
itchat.run()

  
