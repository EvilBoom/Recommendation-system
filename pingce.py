#!/usr/bin/python
# -*- coding: utf-8 -*-

import IO
def pingce(result,test):
    currency=0.0
    recall=0.0
    length=0
    for user in result.keys():
        if len(result[user])==0 :
            length += 1
            continue
        if user in test.keys() and len(test[user])!=0:
            currency=currency+len(set(result[user]) & set(test[user]))/(len(result[user])*1.0)
            recall=recall+len(set(result[user]) & set(test[user]))/(len(test[user])*1.0)
        length=length+1
    currency=currency/length
    recall=recall/length
    return currency,recall

def decrcount(data,count):
    w=dict()
    for key in data.keys():
        w[key]=data[key][0:count]
    return w


def common(result_lmf,result_itemcf):
    w=dict()
    for user in result_lmf.keys():
        if user not in w.keys():
            w[user]=set()
        if user in result_itemcf.keys() and user in result_lmf.keys():
            w[user]=result_lmf[user]&result_itemcf[user]
    return w

def result_add(result_lmf,result_itemcf):
    w=dict()
    for user in result_lmf.keys():
        if user in result_itemcf.keys():
            w[user]=set(result_lmf[user])|set(result_itemcf[user])
    return w




