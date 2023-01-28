import os
import platform
import psutil
import logging
import datetime

from constants import constant


def get_disk_info():
    """
    获取磁盘盘符信息
    :return: 迭代器
    """
    for s_disk_part in psutil.disk_partitions():
        yield s_disk_part


def write2log(msg, log_file=None):
    """
    单次写入日志
    :param msg: 内容
    :param log_file: 文件路径
    """
    if not log_file:
        log_file = constant.LOG_FILE

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write("%s %s" % (current_time, msg) + '\n')


def clean_log(path):
    """
    清空文件内容
    :param path: 文件路径
    """
    with open(path, 'r+') as file:
        file.truncate(0)


def list_folder(path):
    """
    遍历目录
    :param path: 路径
    :return: 迭代器
    """
    try:
        for name in os.listdir(path):
            dir_path = os.path.join(path, name)
            yield dir_path
    except Exception as e:
        error_msg = str(e)
        logging.warning("list_folder:" + error_msg)
        write2log(error_msg, log_file=constant.ERROR_SCAN_LOG_FILE)


def traversal_files(path, depth=0):
    """
    递归遍历目录
    :param path: 路径
    :param depth: 深度
    :return: 文件路径列表、文件夹路径列表
    """
    file_list = list()
    folder_list = list()
    it = list_folder(path)
    for dir_path in it:
        if os.path.isdir(dir_path):
            # 如果是文件夹
            folder_list.append(dir_path)
            if depth != 0:
                _file_list, _folder_list = traversal_files(dir_path, depth=depth - 1)
                file_list = file_list + _file_list
                folder_list = folder_list + _folder_list
        else:
            file_list.append(dir_path)
    return file_list, folder_list


def contain_str_list(file_path, keyword, disks):
    """
    判断文件中是否包含指定字符串，将包含的行加入列表并返回
    :param file_path: 文件
    :param keyword: 被包含的字符串
    :param disks: 指定盘符列表
    :return: 匹配到字符串列表
    """
    result_str_list = list()
    with open(file_path, 'r') as f:
        while True:
            s = f.readline()
            if s is None or s == '':
                break
            s = s.strip()
            file_name = os.path.basename(os.path.normpath(s))
            if keyword in file_name:
                if disks:
                    for ds in disks:
                        if ds == s[0:1].upper():
                            result_str_list.append(s)
                            break

    return result_str_list


def scan_dir(scan_dir_list, depth):
    """
    扫描目录
    :param scan_dir_list: 目录列表
    :param depth: 深度
    """
    clean_log(constant.ERROR_SCAN_LOG_FILE)
    file_op = open(constant.FILE_LIST, "w+")
    folder_op = open(constant.FOLDER_LIST, "w+")
    try:
        for _scan_dir in scan_dir_list:
            file_list, folder_list = traversal_files(_scan_dir, depth=depth)
            for file in file_list:
                try:
                    file_op.write(file + "\n")
                except Exception as e:
                    error_msg = "file_unicode_escape:" + file.encode('unicode_escape').decode() + " error:" + str(e)
                    try:
                        write2log(error_msg, log_file=constant.ERROR_SCAN_LOG_FILE)
                    except Exception as e1:
                        logging.error(e1)
            file_op.flush()
            for folder in folder_list:
                try:
                    folder_op.write(folder + "\n")
                except Exception as e:
                    error_msg = "file_unicode_escape:" + folder.encode('unicode_escape').decode() + " error:" + str(e)
                    try:
                        write2log(error_msg, log_file=constant.ERROR_SCAN_LOG_FILE)
                    except Exception as e1:
                        logging.error(e1)
            folder_op.flush()
    finally:
        file_op.close()
        folder_op.close()


def path_str_format(s):
    if platform.system() == 'Windows':
        s = s.replace('/', '\\', 1)
    return s


def search_by_keyword(keyword, disks=None):
    result_file_list = contain_str_list(constant.FILE_LIST, keyword, disks)
    result_folder_list = contain_str_list(constant.FOLDER_LIST, keyword, disks)
    return result_file_list, result_folder_list
