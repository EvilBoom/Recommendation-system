#!/usr/bin/python
# -*- coding: utf-8 -*-
#对离散变量进行推荐

import IO
import math


datas_pre="datas/"
results_pre="results/"
logs_pre="logs/"

#core function

#连续变量相似度



def mangli(train,totl_items):
    w=dict()
    N=dict()
    for item in totl_items:
        w[item]=dict()
        for item_ in totl_items:
            w[item][item_]=0
    for user,items in train.items():
        for item in items:
            if item not in N.keys():
                N[item]=0
            N[item]+=1
            for item_ in items:
                if item_ != item:
                    w[item][item_]+=1
    return w,N

def getsimmatrix(public,N,totl_items):
    w=dict()
    for item in totl_items:
        w[item]=dict()
        for item_ in totl_items:
            if item_!=item:
                w[item][item_]=public[item][item_]/math.sqrt(N[item]*N[item_])
    return w

def getksimneib(public,neber):
    w=dict()
    for row,cols in public.items():
        w[row]=dict()
        cols=sorted(public[row].items(),key=lambda d:d[1],reverse=True)[0:neber]
        for tuple_ in cols:
            w[row][tuple_[0]]=tuple_[1]
    return w

def getrecommanditems(sim_person,user_item_dict,K):
    w=dict()
    for user,items in user_item_dict.items():
        w[user]=dict()
        for item in items:
            for re_item,re_item_value in sim_person[item].items():
                if re_item not in user_item_dict[user]:
                    if re_item not in w[user].keys():
                        w[user][re_item]=0.0
                    w[user][re_item]+=re_item_value
        temps=sorted(w[user].items(),key=lambda d:d[1],reverse=True)[0:K]
        w[user].clear()
        w[user]=set()
        for key,value in temps:
            w[user].add(key)
    return w


def change2dictset(recomdata):
    w=dict()
    for key,item in recomdata.items():
        if key not in w.keys():
            w[key]=set()
        for x, value in item:
            w[key].add(x)
    return w


def itemcf(train,totl_items,reitem_count):
    C, N = mangli(train, totl_items)
    matrix = getsimmatrix(C, N, totl_items)
    kneber = getksimneib(matrix, 10)
    result = getrecommanditems(kneber, train, reitem_count)
    IO.writeresult(result,filepath=results_pre+"itemcf_result.csv")

def test():
    test,train,totl_items=IO.just_read_train_test(pre="datas/")












    
    
    











    