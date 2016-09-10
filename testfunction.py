#!/usr/bin/python
#-*-coding:utf-8-*-
import IO
import recommendation
import pingce
import hotitemsrecommandation
datas_pre="datas/"
results_pre="results/"
logs_pre="logs/"
#recommendation.recommendation()
def common(result_lmf,result_itemcf):
    w=dict()
    for user in result_lmf.keys():
        if user not in w.keys():
            w[user]=set()
        if user in result_itemcf.keys() and user in result_lmf.keys():
            w[user]=set(result_lmf[user])&set(result_itemcf[user])
    return w

def result_add(result_lmf,result_itemcf):
    w=dict()
    for user in result_lmf.keys():
        if user in result_itemcf.keys():
            w[user]=set(result_lmf[user])|set(result_itemcf[user])
    return w
def result_sorted(result,k):
    w=dict()
    for key, values in result.items():
        w[key]=result[key][0:k]
    return w
def result_test_common(result,test):
    file=open(results_pre+"result_test_common.csv","w")
    for key,value in test.items():
        file.write(key+":"+str(len(test[key]&result[key]))+":"+str(len(test[key]))+"\n")
    file.flush()
    file.close()
#对推荐结果进行分析

#lmf和itemcf的交集
def bestronghe_1():
    result_lmf = IO.readcsv_list(filepath=results_pre + "lmf_result.csv")
    result_itemcf = IO.readcsv_list(filepath=results_pre + "itemcf_result.csv")
    result_usercf = IO.readcsv_list(filepath=results_pre + "usercf_result.csv")
    test = IO.readcsv(datas_pre + "test.csv")
    totl_users=IO.read_oneline_list(datas_pre+"users.csv")
    hotitem=IO.read_oneline_list(results_pre+"hotitems.csv")
    re_1_1 = result_sorted(result_lmf, 4)
    re_2_1 = result_sorted(result_itemcf, 4)
    re_3_1 = result_sorted(result_usercf, 4)
    re = result_add(re_1_1, re_2_1)
    re = result_add(re, re_3_1)
    #result_test_common(re, test)
    for user in totl_users:
        if user not in re.keys():
            re[user] = hotitemsrecommandation.hotitem(hot_items=hotitem, N=12)
    IO.write_key_list_dict(re, filepath=results_pre + "common.csv")
    print "itemcf:" + str(pingce.pingce(result_itemcf, test))
    print "lmf:" + str(pingce.pingce(result_lmf, test))
    print "usercf:" + str(pingce.pingce(result_usercf, test))
    print pingce.pingce(re, test)
if __name__=="__main__":
    bestronghe_1()
