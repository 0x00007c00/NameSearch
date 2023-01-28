# -*- coding: utf-8 -*-

import datetime
import os
import time

RGX = "%Y-%m-%d %H:%M"


def get_last_modification_time(file_path):
    """
    获取文件最后一次被修改的时间
    :param file_path: 文件路径
    :return: 时间
    """
    info_obj = os.stat(file_path)
    mtime = info_obj.st_mtime
    return time.strftime(RGX, time.localtime(mtime))


def get_next_day(str_time, n):
    """
    获取指定日期的后n天
    :param str_time: 字符串日期
    :param n: 后几天
    :return: 字符串日期结果
    """
    _datetime = datetime.datetime.strptime(str_time, RGX)
    return (_datetime + datetime.timedelta(days=+n)).strftime(RGX)


def get_now_time(rgx=None):
    """
    获取当前日期字符串
    :return: 字符串日期
    """
    if not rgx:
        rgx = RGX
    return datetime.datetime.now().strftime(rgx)


def date_str_compare(d1, d2):
    """
    两个字符串日期比较大小
    :param d1: 日期1
    :param d2: 日期2
    :return: 日期1 > 日期2 返回 True
    """
    d1_datetime = datetime.datetime.strptime(d1, RGX)
    d2_datetime = datetime.datetime.strptime(d2, RGX)
    return d1_datetime > d2_datetime


def cnt_differ_days(d1, d2):
    """
    计算d1比d2大几天
    :param d1: 字符串日期1
    :param d2: 字符串日期2
    :return: 天数
    """
    d1_datetime = datetime.datetime.strptime(d1, RGX)
    d2_datetime = datetime.datetime.strptime(d2, RGX)
    return (d1_datetime - d2_datetime).days
