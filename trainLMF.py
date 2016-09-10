#!/usr/lib/python
#-*-coding:utf-8-*-
import LMF
import pingce
import IO
import time
pre="traindatas/"
result_pre="trainresult/"
log_pre="logs/"


def run_consin(train,test,number,hotitem,traintimes=100,alpha=0.02,lamda=1,runtimes=4):
    msg=str()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    msg="===================start:" + str(now) + "=========================\r\n"

    msg=msg+"因子数量=" + str(number) + "\r\n" + "训练次数" + str(traintimes) + "\r\n" + "alpha=" + str(
        alpha) + "\r\n" + "lamda=" + str(lamda) + "\r\n循环次数="+str(runtimes)+"\r\n"

    # IO.write_key_list_dict(train, "train.csv")
    # IO.write_key_list_dict(test, "test.csv")

    msg = msg+ "用户数："+str(len(train))+"   物品数："+str(len(hotitem))+"\r\n"
    currency_totl,recall_totl=0.0,0.0
    for i in range(0,runtimes):
        [P, Q] = LMF.initmodel(train, number)
        train_ = LMF.caiyang(train, hotitem)
        [P, Q] = LMF.lmf(train_, number, traintimes, alpha, P, Q, lamda)
        IO.write_key_list_dict(P, result_pre+str(i+1)+"p.csv")
        IO.write_key_list_dict(Q, result_pre+str(i+1)+"q.csv")

        # temp=LMF.getmax_larten(P,Q,number)
        # IO.write_dict_dict(temp,filepath="temp.csv")
        # print testfunction.read(P,Q,number)

        currency,recall=result_consin(P, Q, train ,test,  15,i)
        currency_totl+=currency
        recall_totl+=recall

    msg=msg+"平均准确率:"+str(currency_totl/runtimes)+",    平均召回率:"+str(recall_totl/runtimes)+"\r\n"
    IO.log(filepath=log_pre+"log.txt",msg=msg)

def result_consin(P,Q,train,test,resy_count,i):
    result = LMF.content_recommendation(P, Q, train, resy_count)
    bzresult = LMF.oresult_to_bzresult(result)
    IO.write_key_list_dict(bzresult,result_pre+str(i+1)+"_result.csv")
    currency,recall = pingce.pingce(bzresult, test)
    return  currency,recall

def result(P,Q,train,test,resy_count,i):
    result = LMF.content_recommendation(P, Q, train, resy_count)
    bzresult = LMF.oresult_to_bzresult(result)
    IO.write_key_list_dict(bzresult,result_pre+str(i+1)+"_result.csv")
    currency,recall = pingce.pingce(bzresult, test)
    return  currency,recall


def run_once(train,test,hotitem,number=30,traintimes=100,alpha=0.02,lamda=0.01):
    msg = str()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    msg = "===================start:" + str(now) + "=========================\r\n"
    msg = msg + "因子数量=" + str(number) + "\r\n" + "训练次数" + str(traintimes) + "\r\n" + "alpha=" + str(
        alpha) + "\r\n" + "lamda=" + str(lamda) + "\r\n"
    msg = msg + "用户数：" + str(len(train)) + "   物品数：" + str(len(hotitem)) + "\r\n"

    [P, Q] = LMF.initmodel(train, number)
    train_ = LMF.caiyang(train, hotitem)
    [P, Q] = LMF.lmf(train_, number, traintimes, alpha, P, Q, lamda)
    IO.write_key_list_dict(P, result_pre + "p.csv")
    IO.write_key_list_dict(Q, result_pre + "q.csv")
    currency_totl, recall_totl = result_consin(P, Q, train, test, 15,0)
    msg = msg + "平均准确率:" + str(currency_totl) + ",    平均召回率:" + str(recall_totl) + "\r\n"
    IO.log(filepath=log_pre + "log.txt", msg=msg)

def run():
    #test, train, totl_item = IO.train_test_product(filepath="data.csv",pre="datas/",maxline=1000000,rows=3)
    test,train,totl_item=IO.just_read_train_test(pre=pre)
    item_hot = LMF.item_and_hot(train)
    run_once(train,test,number=30,hotitem=item_hot,traintimes=40,alpha=0.02,lamda=0.5)

if __name__=="__main__":
    run()