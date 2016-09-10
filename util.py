#!/usr/bin/python
#-*-coding:utf-8-*-
import IO
def matrix_product(user_item_dict,totl_items):
    for user,items in user_item_dict.items():
        for item in totl_items:
            if item not in items.keys():
                user_item_dict[user][item]=0

test,train,totl_items=IO.just_read_train_test(pre="datas/")
matrix_product(train,totl_items)
print train[5988][2860]

