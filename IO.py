#!/usr/lib/python
#-*-coding:utf-8-*-
import random
import time

#io function

#临时格式转换函数
def formatchagne():
    f=open("datas/users.dat","r")
    w=open("datas/users.csv","w")
    line=f.readline()
    lines = line.split("::")
    w.write(lines[0])
    line = f.readline()
    while line!="":
        lines = line.split("::")
        if len(lines)<1:
            continue
        w.write(","+lines[0])
        line=f.readline()
    f.close()
    w.flush()
    w.close()

def formatchagne1():
    f=open("datas/user_info_format1.csv","r")
    w=open("datas/alibabadata_users.csv","w")
    f.readline()
    line=f.readline()
    lines = line.split(",")
    w.write(lines[0])
    line = f.readline()
    while line!="":
        lines = line.split(",")
        if len(lines)<1:
            continue
        w.write(","+lines[0])
        line=f.readline()
    f.close()
    w.flush()
    w.close()

def formatchagnedatas():
    f=open("datas/user_log_format1.csv","r")
    w=open("datas/alibaba_data.csv","w")
    line=f.readline()
    flag=0
    while flag<10000000 and line!="":
        if flag==0:
            flag += 1
            line = f.readline()
            continue
        lines = line.split(",")
        if len(lines)<1:
            continue
        w.write(lines[0]+","+lines[1]+"\n")
        line=f.readline()
        flag+=1
    f.close()
    w.flush()
    w.close()

def writeresult(result,filepath="result.csv"):
    f=open(filepath,"w")
    for key,values in result.items():
        f.write(str(key))
        for value in values:
            f.write(","+str(value))
        f.write("\r\n")
    f.flush()
    f.close()

#生成训练集和测试集的函数(datas/)
def train_test_product(filepath,rows,pre="",maxline=1000000):
    filepath=pre+filepath
    totl_items = set()
    test = dict()
    train = dict()
    f = open(filepath, "r")
    flag = 0
    random.seed(int(time.time()))
    line = f.readline()
    while flag < maxline and line != "":
        line = line.rstrip("\n")
        line = line.rstrip("\r")
        lines = line.split(",")
        flag = flag + 1
        if len(lines) < rows:
            continue
        if random.randint(1, 10) < 9:
            if lines[0] not in train.keys():
                train[lines[0]] = dict()
            train[lines[0]][lines[1]] = int(lines[2])*1.0
        else:
            if lines[0] not in test.keys():
                test[lines[0]] = dict()
            test[lines[0]][lines[1]] = int(lines[2])*1.0
        totl_items.add(lines[1])
        line = f.readline()
    train_file = open(pre+"train.csv","w")
    test_file = open(pre+"test.csv", "w")
    for user,items in train.items():
        train_file.write(user)
        for item,value in items.items():
            train_file.write(","+item+":"+str(value))
        train_file.write("\r\n")
    for user, items in test.items():
        test_file.write(user)
        for item, value in items.items():
            test_file.write("," + item + ":" + str(value))
        test_file.write("\r\n")
    f.close()
    train_file.flush()
    test_file.flush()
    train_file.close()
    test_file.close()
    return test, train, totl_items

#读取训练集的函数
def just_read_train_test(pre,trainpath="train.csv",testpath="test.csv"):
    train_file=open(pre+trainpath,"r")
    test_file=open(pre+testpath,"r")
    line=train_file.readline()
    train=dict()
    totl_item = set()
    while line != "":
        line = line.rstrip("\n")
        line = line.rstrip("\r")
        lines = line.split(",")
        if lines[0] not in train.keys():
            train[lines[0]]=dict()
        for i in range(1,len(lines)):
            item,value=lines[i].split(":")
            train[lines[0]][item]= float(value)*1.0
            totl_item.add(item)
        line = train_file.readline()
    test = dict()
    line = test_file.readline()
    while line != "":
        line = line.rstrip("\n")
        line = line.rstrip("\r")
        lines = line.split(",")
        if lines[0] not in test.keys():
            test[lines[0]] = dict()
        for i in range(1, len(lines)):
            item, value = lines[i].split(":")
            test[lines[0]][item] = float(value)*1.0
            totl_item.add(item)
        line = test_file.readline()
    return test,train,totl_item

#读取csv文件，返回dict("key":set())
def readcsv(filepath):
    w=dict()
    file = open(filepath, "r")
    line=file.readline()
    while line != "":
        line = line.rstrip("\n")
        line = line.rstrip("\r")
        lines = line.split(",")
        if lines[0] not in w.keys():
            w[lines[0]] = set()
        for i in range(1, len(lines)):
            w[lines[0]].add(lines[i])
        line = file.readline()
    return w

#读取csv文件，返回dict("key":list())
def readcsv_list(filepath):
    w=dict()
    file = open(filepath, "r")
    line=file.readline()
    while line != "":
        line = line.rstrip("\n")
        line = line.rstrip("\r")
        lines = line.split(",")
        if lines[0] not in w.keys():
            w[lines[0]] = list()
        for i in range(1, len(lines)):
            w[lines[0]].append(lines[i])
        line = file.readline()
    return w

#写出格式为 dict("key":list())文件
def write_key_list_dict(data,filepath="data.csv"):
    f=open(filepath,'w')
    for key,items in data.items():
        f.write(str(key))
        for item in items:
            f.write(","+str(item))
        f.write('\n')

def hotitem2bzhotitem(hot_item):
    w=list()
    for tuples in hot_item:
        w.append(tuples[0])
    return w

#读取单行记录
def read_oneline_set(filepath,maxline=-1):
    file = open(filepath, "r")
    line=file.readline()
    file.close()
    if maxline<=0:
        return set(line.split(","))
    else:
        return set(line.split(",")[0:maxline])

def read_oneline_list(filepath,maxline=-1):
    file=open(filepath,"r")
    line=file.readline()
    file.close()
    if maxline <= 0:
        return line.split(",")
    else:
        return line.split(",")[0:maxline]


#写出单行记录
def write_oneline_list(filepath,data):
    file=open(filepath,"w")
    file.write(data[0])
    for i in range(1,len(data)):
        file.write(","+data[i])
    file.flush()
    file.close()


#for trainLMF logs
def log(filepath,msg):
    file=open(filepath,"a")
    file.write(msg)
    file.flush()
    file.close()
#test function

#train_test_product(filepath="data.csv",rows=3,pre="datas/")

#a,b,c=just_read_train_test(pre="datas/")
# print read_oneline_set("datas/users.csv")

# print read_oneline_list("datas/users.csv")


#formatchagne1()
#formatchagnedatas()
# test, train, totl_items=train_test_product(pre="datas/",filepath="alibaba_data.csv",maxline=100000)
# print len(train),len(totl_items)

# print read_oneline_list("datas/users.csv")

