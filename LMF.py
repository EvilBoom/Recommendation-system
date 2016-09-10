#!/usr/lib/python
#-*- coding:utf8 -*-
import random
import math
import IO
import time

datas_pre="datas/"
results_pre="results/"
logs_pre="logs/"


#核心功能函数
#初始化P,Q矩阵，返回类型dict("key":list(),)
def initmodel(user_items,F):
    P=dict()
    Q=dict()
    for user,items in user_items.items():
        if user not in P.keys():
            P[user]=list()
            i=0
            for i in range(0,F):
                P[user].append(random.uniform(0,1))
        for item in items:
            if item not in Q.keys():
                Q[item] = list()
                i = 0
                for i in range(0, F):
                    Q[item].append(random.uniform(0,1) )
    return P,Q


#算出热门商品，返回类型 dict("item_id":"show_times",)
def item_and_hot(user_item):
    re=dict()
    for key,value in user_item.items():
       for item in value:
           if item not in re.keys():
               re[item] = 0
           re[item] = re[item] + 1
    re = sorted(re.iteritems(),key=lambda d: d[1], reverse=True)
    return re

#根据现有的P,Q矩阵对user对item购买行为进行一个预测
def predict(P,Q,user,item,F):
    #不健壮
    i=0
    re=0
    for i in range(0,F):
        #print str(user+":"+item)
        re=re+P[user][i]*Q[item][i]
    return re

#从train中采集样本（负样本、正样本），为每个用户采集rating=1:1的正负向本,返回类型:dict("user":dict("item":0/1,...),...)
def caiyang(train,hot_item):
    re=train
    #正样本为购买过的所有的物品总和
    #负样本为热门商品中的每购买过的商品
    for user,items in train.items():
        i=0
        z=len(items)
        for i in range(0, len(items) * 3):
            item = hot_item[random.randint(0,len(hot_item)-1)][0]
            if item not  in re[user].keys():
                re[user][item]=0
    return re
#梯度下降函数
def lmf(train,F,N,alpha,P,Q,lamda):
    for setup in range(0,N):
        totoleui=0
        for user,items in train.items():
            if random.randint(1, 10) == 9:
                for item,value in items.items():
                    #print value,predict(P,Q,user,item,F)
                    eui=value-predict(P,Q,user,item,F)
                    totoleui=totoleui+abs(eui)
                    oldp=P[user]
                    oldq=Q[item]
                    for i in range(0,F):
                        P[user][i] = oldp[i] + alpha * (eui * oldq[i] - lamda * oldp[i])
                        Q[item][i] = oldq[i] + alpha * (eui * oldp[i] - lamda * oldq[i])
        alpha=alpha*0.9
    return P,Q
#直接根据P,Q的内积进行推荐（前面用的余弦相似度）
def content_recommendation_2(P,Q,user_item,count=10):
    re=dict()
    for user,its in P.items():
        re[user]=dict()
        for item,itss in Q.items():
            if item not in user_item[user]:
                i=0
                temp=0
                for i in range(0,len(its)):
                    temp=temp+P[user][i]*Q[item][i]
                re[user][item]=temp
        re[user] = sorted(re[user].items(), key=lambda d: d[1], reverse=True)[0:count]
        #print re[user]
    return re
#余弦相似度计算P中与Q中相似的用户-商品，得到推荐结果
def content_recommendation(P,Q,user_item,count=10):
    re=dict()
    for user,its in P.items():
        re[user]=dict()
        for item,itss in Q.items():
            if item not in user_item[user]:
                i=0
                xy=0
                xx=0
                yy=0
                for i in range(0,len(its)):
                    xy=xy+its[i]*itss[i]
                    xx=xx+its[i]*its[i]
                    yy=yy+itss[i]*itss[i]
                con=xy/(math.sqrt(xx)*math.sqrt(yy))
                re[user][item]=con
        re[user]=sorted(re[user].items(),key=lambda d:d[1],reverse=True)[0:count]

    return re

#其他函数部分
#将原始推荐结果转换为标准结果
def oresult_to_bzresult(result):
    re=dict()
    for key,value in result.items():
        re[key]=list()
        for vlaue_ in value:
            re[key].append(vlaue_[0])
    return re

#获得每个因子较大的前几个item
def getmax_larten(P,Q,number):
    maxmovies=dict()
    flag=0
    for flag in range(0,number):
        maxmovies[flag]=dict()
        for key,values in Q.items():
            maxmovies[flag][key]=values[flag]
        maxmovies[flag]=sorted(maxmovies[flag].items(),key=lambda d:d[1],reverse=True)[0:5]
    return maxmovies

#随机抽样P，Q检验，数量为10
def randomcheckPQ(P,Q):
    re_p="P:\r\n"
    re_q="Q:\r\n"
    random.seed(int(time.time()))
    list_p = random.sample(range(0,len(P)),10)
    list_q = random.sample(range(0, len(Q)), 10)
    for i in list_p:
        re_p += P.keys()[i] + ":" + str(P[P.keys()[i]]) + "\r\n"
    for i in list_q:
        re_q += Q.keys()[i] + ":" + str(Q[Q.keys()[i]]) + "\r\n"
    return re_p+re_q

def run(train,test,number,hotitem,traintimes=100,alpha=0.02,lamda=1):
    [P, Q] = initmodel(train, number)
    train_ = caiyang(train, hotitem)
    [P, Q] = lmf(train_, number, traintimes, alpha, P, Q, lamda)
    IO.write_key_list_dict(P,results_pre+"p.csv")
    IO.write_key_list_dict(Q,results_pre+"q.csv")
    result_consin(P,Q,train,15)

def result_consin(P,Q,train,resy_count):
    result = content_recommendation(P, Q, train, resy_count)
    bzresult = oresult_to_bzresult(result)
    IO.write_key_list_dict(bzresult,results_pre+"lmf_result.csv")

def LMF(test, train,number=30,traintimes=100,alpha=0.02,lamda=1):
    item_hot = item_and_hot(train)
    bzitem_hot=IO.hotitem2bzhotitem(item_hot)
    IO.write_oneline_list(results_pre+"hotitems.csv",bzitem_hot)
    run(train, test, number=number, hotitem=item_hot, traintimes=traintimes, alpha=alpha, lamda=lamda)
    return bzitem_hot


