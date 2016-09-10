#!/usr/lib/python
#-*-coding:utf-8-*-
import LMF
import IO
import itemcf
import usercf
import hotitemsrecommandation

datas_pre="datas/"
results_pre="results/"
logs_pre="logs/"

def recommendation():

    test, train,totl_items=IO.train_test_product(filepath="data.csv", pre=datas_pre, maxline=10000,rows=3)
    #test, train, totl_items=IO.just_read_train_test(pre=datas_pre)
    itemcf.itemcf(train,totl_items,15)
    usercf.usercf(test, train,totl_items,re_count=80)
    LMF.LMF(test, train,number=30,traintimes=100,alpha=0.02,lamda=0.01)


def rongghe(result_lmf,result_itemcf,result_usercf,x,y,z,K,totl_users,hotitem):

    w=dict()
    for user,items in result_lmf.items():
        if user not in w.keys():
            w[user]=dict()
        for item in items:
            if item not in w[user].keys():
                w[user][item]=0.0
    for user, items in result_usercf.items():
        if user not in w.keys():
            w[user] = dict()
        for item in items:
            if item not in w[user].keys():
                w[user][item] = 0.0
    for user, items in result_itemcf.items():
        if user not in w.keys():
            w[user] = dict()
        for item in items:
            if item not in w[user].keys():
                w[user][item] = 0.0

        temp=sorted(w[user].items(),key=lambda d:d[1],reverse=True)[0:K]
        w[user]=list()
        for temps in temp:
           w[user].append(temps[0])
    for user in totl_users:
        if user not in w.keys():
            w[user]=hotitemsrecommandation.hotitem(hot_items=hotitem,N=K)
    return w