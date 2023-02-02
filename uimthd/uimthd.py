# -*- coding: utf-8 -*-

import threading
import configparser
import os

from mthd import core
from uimthd import utils
from constants import constant


def save_checked_status(unchecked_list):
    """
    保存盘符复选框状态
    :param unchecked_list: 被取消选中的盘符
    """
    s = ''
    for unchecked in unchecked_list:
        s += unchecked + ','
    if s.endswith(','):
        s = s[0:-1]
    config = configparser.ConfigParser()
    config.read(constant.CONFIG_PATH, encoding="utf-8")
    config.set("checkbox", "unchecked", s)
    config.write(open(constant.CONFIG_PATH, "w"))


def config_read(header, key):
    """
    读取配置文件
    :param header: 节点名称
    :param key: 属性名
    :return:
    """
    config = configparser.ConfigParser()
    config.read(constant.CONFIG_PATH, encoding="utf-8")
    value = config[header][key]
    return value


def config_write(header, key, val):
    """
    修改配置
    :param header: 节点名称
    :param key: 属性名
    :param val: 值
    """
    config = configparser.ConfigParser()
    config.read(constant.CONFIG_PATH, encoding="utf-8")
    config.set(header, key, val)
    config.write(open(constant.CONFIG_PATH, "w"))


def scan_all_disk_part():
    """
    全盘扫描
    """
    depth = config_read('depth', 'depth')
    if not depth:
        depth = 5

    scan_dist_part_list = []
    s_disk_part_iter = core.get_disk_info()
    for disk_part in s_disk_part_iter:
        if disk_part.fstype:
            scan_dist_part_list.append(disk_part.device)
    t1 = threading.Thread(target=core.scan_dir, args=(scan_dist_part_list, int(depth)))
    t1.start()
    return t1


def set_all_enabled(win, b):
    """
    将窗口内容设置为可操作/不可操作
    :param win: 窗口对象
    :param b: boolean状态
    """
    win.queryEdit.setEnabled(b)
    win.pushButton.setEnabled(b)
    win.scan_button.setEnabled(b)


def search_thread(keyword, checked_dist_part_list, rst_lst):
    print("checked_dist_part_list", checked_dist_part_list)
    result_file_list, result_folder_list = core.search_by_keyword(keyword, disks=checked_dist_part_list)
    for result_file in result_file_list:
        result_file = core.path_str_format(result_file)
        rst_lst.append("文件：" + result_file)
    for result_folder in result_folder_list:
        result_folder = core.path_str_format(result_folder)
        rst_lst.append("文件夹：" + result_folder)
    if len(rst_lst) == 0:
        rst_lst.append("无结果")
        print("Search ended, no results found")
    else:
        print("Search ended, %d results were found" % len(rst_lst))


def search(keyword, checked_dist_part_list, rst_lst):
    """
    查询结果，并显示
    :param keyword: 查询关键字
    :param checked_dist_part_list: 查询磁盘列表
    """
    t1 = threading.Thread(target=search_thread, args=(keyword, checked_dist_part_list, rst_lst))
    t1.start()
    return t1


def check_update_list(check_types=(0, 1, 2)):
    """
    检查扫描列表是否需要更新
    @:param check_types 检测的类型
    """
    check = False
    update_type = 0
    config_scan_next_day = config_read('user', 'scan_next_day')
    last_time = None
    overdue = None
    msg = None
    if 0 in check_types and not os.path.exists(constant.FILE_LIST):
        # 数据文件不存在则为首次使用
        check = True
        update_type = 0
        msg = "首次使用，是否现在就开始全盘扫描？"
    else:
        last_time = utils.get_last_modification_time(constant.FILE_LIST)
        set_scan_day = utils.get_next_day(last_time, int(config_scan_next_day))
        if 1 in check_types and utils.date_str_compare(utils.get_now_time(), set_scan_day):
            # 长时间未更新
            check = True
            update_type = 1
            overdue = utils.cnt_differ_days(utils.get_now_time(), last_time)
            msg = "距离上次全盘扫描已超过%s天，是否重新进行全盘扫描？" % overdue
        else:
            with open(constant.FILE_LIST, 'r') as f:
                s = f.readline()
                if 2 in check_types and s is None or s == '':
                    # 数据文件内容为空
                    check = True
                    update_type = 2
                    msg = '文件列表异常，需要重新扫描磁盘，是否现在开始？'

    return check, update_type, last_time, overdue, msg
