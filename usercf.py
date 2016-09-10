# -*- coding: utf-8 -*-

datas_pre="datas/"
results_pre="results/"
logs_pre="logs/"

from math import sqrt
import IO

#core function
def cosin(list_1,list_2):
    i=0
    xy,x,y=0,0,0
    x=sqrt(sum(pow(item,2) for item in list_1))
    y=sqrt(sum(pow(item,2) for item in list_2))
    while i<len(list_1):
        xy=xy+list_1[i]*list_2[i]
        i=i+1
    return xy/(x*y*1.0)

def sim_cosin_lisan(list_1,list_2):
    comm=0
    for x in list_1:
        if x in list_2:
            comm=comm+1
    #print comm,list_1,list_2
    return round(comm/(sqrt(len(list_1)*len(list_2))*1.0),2)

def sim_cosin_lisan_set(set_1,set_2):
    comm=len(set(set_1) & set(set_2))
    return round(comm/(sqrt(len(set_1)*len(set_2))*1.0),2)

def sim_cosin(list_1,list_2):
    c=cosin(list_1,list_2)
    return 1/(1+c)

def mangli(train):
    w=dict()
    for u,items_u in train.items():
        if u not in w.keys():
            w[u]=dict()
        for v,items_v in train.items():
            if u==v :
                w[u][v]=0
            else:
                w[u][v]=sim_cosin_lisan_set(items_u,items_v)
    return w

def getksim(data,k):
    w=dict()
    for user,others in data.items():
        temp=sorted(data[user].items(),key=lambda d:d[1],reverse=True)[0:k]
        w[user]=dict()
        for tuple_ in temp:
            w[user][tuple_[0]] = tuple_[1]
    return w

def getksim_oneperson(sim_dict,k,person):
    re=list()
    temp=sorted(sim_dict.items(),key=lambda d:d[1],reverse=True)[0:4]
    for x in temp:
        if x!=person:
            re.append(x)
    return re

def getrecommanditems(sim_person,user_item_dict,k):
    w = dict()
    for user in sim_person.keys():
        w[user]=dict()
        for other,sim_other in sim_person[user].items():
            for item in user_item_dict[other]:
                if item not in w[user].keys():
                    w[user][item]=0.0
                w[user][item]+=sim_other
        temps = sorted(w[user].items(), key=lambda d: d[1], reverse=True)[0:k]
        w[user].clear()
        w[user] = list()
        for key, value in temps:
            w[user].append(key)
    return w


def change2dictset(recomdata):
    w=dict()
    for key, item in recomdata.items():
        if key not in w.keys():
            w[key]=set()
        for x, value in item:
            w[key].add(x)
    return w
def usercf(train,test,totl_item,re_count=80):
    sim_data=mangli(train)
    #IO.write_dict_dict(sim_data,"usermatrix.csv")
    sim_person=getksim(sim_data,re_count)
    recommanddata=getrecommanditems(sim_person,train,re_count)
    IO.write_key_list_dict(recommanddata,results_pre+"usercf_result.csv")













    
    
    











    