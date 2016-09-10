#!/usr/bin/python
#-*-coding:utf-8-*-
import math

def cosin(list_1,list_2):
    i=0
    xy,x,y=0,0,0
    x=math.sqrt(sum(pow(item,2) for item in list_1))
    y=math.sqrt(sum(pow(item,2) for item in list_2))
    while i<len(list_1):
        xy=xy+list_1[i]*list_2[i]
        i=i+1
    return xy/(x*y*1.0)
def consin_dict(user_items_dict,totl_items):
    w=dict()
    for user in user_items_dict.keys():
        if user not in w.keys():
            w[user] = dict()
        for other in user_items_dict.keys():
            if user != other:
                if other not in w[user].keys():
                    w[user][other]=0.0
                x,y,xy=0,0,0
                for items in totl_items:
                    xy=user_items_dict[user]*user_items_dict[other]
                    x=user_items_dict[user]*user_items_dict[user]
                    y=user_items_dict[other] * user_items_dict[other]
                x=math.sqrt(x)
                y=math.sqrt(y)
                w[user][other]=round(xy/(x*y*1.0),3)
    return w
#离散变量list相似度
def sim_cosin_lisan(list_1,list_2):
    comm=0
    for x in list_1:
        if x in list_2:
            comm=comm+1
    #print comm,list_1,list_2
    return round(comm/(math.sqrt(len(list_1)*len(list_2))*1.0),2)

#离散变量set相似度
def sim_cosin_lisan_set(set_1,set_2):
    comm=len(set_1 & set_2)
    return round(comm/(math.sqrt(len(set_1)*len(set_2))*1.0),2)