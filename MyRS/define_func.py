# -*- coding: utf-8 -*-

import pandas as pd


def data_split(df, col, symbol):
    """

    :param df: 数据帧
    :param col: 分裂所在的列名
    :param symbol: 分裂字符“;”,“,”等
    :return:
    """
    split = col + '_split'
    # num = col + '_num'
    # print(df[col])
    df[split] = df[col].str.split(symbol)
    # print(df[split])
    # df[num] = df[[split]].apply(lambda z:len(z[split]), axis=1)
    df_split = df.explode(split)
    # print(df_split.shape)
    return df_split


def data_combine(df, col_group, col_combine, symbol, mode=1):
    """

    :param df: 数据帧
    :param col_group: 分组列
    :param col_combine: 聚合列
    :param symbol: 聚合连接字符
    :param mode:是否删除重复值，1为删除，0为不删除
    :return:
    """
    df_new = df[[col_group, col_combine]]
    if mode == 1:
        df_new.drop_duplicates(subset=None, keep='first', inplace=True)
        df_new = df_new.sort_values(by=[col_combine], ascending=True, axis=0)

    df_new[col_combine] = df_new[col_combine].astype('str')
    df_new = df_new.groupby(col_group)[col_combine].apply(lambda z: z.str.cat(sep=symbol)).reset_index()
    del df[col_combine]
    # df_new.to_excel("df_new.xlsx")
    df = pd.merge(df, df_new, how='left', on=col_group)
    # df.to_excel("df.xlsx")
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    return df


def vlookup(df1, df2, list1, how1, axis1=0):
    if type(list1) == list:
        df_new = pd.merge(df1, df2.loc[:, list1], how=how1, axis1=axis1)
    else:
        df_new = pd.merge(df1, df2, how=how1, axis1=axis1)
    return df_new


def str_replace(str1, symbol):
    """

    :param str1: 字符串
    :param symbol: 截取的字符
    :return:
    :rtype: 字符串str1截取，截取某字符串symbol前面的字符，包括本字符串的第一个字符
    """
    num = len(str1)
    if str1.find(symbol) >= 0:
        str1 = str1[:str1.find(symbol) + 1]
    else:
        str1 = str1[:num + 1]
    return str1
