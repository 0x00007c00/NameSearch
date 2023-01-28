# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import QStringListModel, QTimer
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from constants import constant
from mthd import core
from ui import KsUI
from uimthd import uimthd
from uimthd import utils


# from PyQt5 import QtWidgets, uic


class MainDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.task_scan_all_disk_part = None
        self.scan_state = 0
        self.task_search = None
        self.search_state = 0
        self.rst_lst = list()
        self.ui = KsUI.Ui_Widget()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.search)
        self.ui.queryEdit.returnPressed.connect(self.search)
        self.ui.scan_button.clicked.connect(self.scan_all_disk_part)
        self.setWindowTitle('Fast查询')
        self.setWindowIcon(QIcon('img/tb.jpg'))
        self.setFixedSize(self.width(), self.height())

        self.ui.checkBox_C.hide()
        self.ui.checkBox_D.hide()
        self.ui.checkBox_E.hide()
        self.ui.checkBox_F.hide()
        self.ui.checkBox_G.hide()
        self.ui.checkBox_H.hide()
        self.ui.checkBox_I.hide()
        self.ui.checkBox_J.hide()
        self.ui.checkBox_K.hide()
        self.ui.checkBox_L.hide()
        for _disk_part in dist_part_list:
            eval("self.ui.checkBox_" + _disk_part + ".show()")

        unchecked = uimthd.config_read('checkbox', 'unchecked')
        if unchecked:
            for unchecked_part in unchecked.split(','):
                if unchecked_part:
                    eval("self.ui.checkBox_" + unchecked_part + ".setChecked(False)")

        self.ui.checkBox_C.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_D.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_E.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_F.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_G.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_H.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_I.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_J.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_K.stateChanged.connect(lambda: self.change_check_box())
        self.ui.checkBox_L.stateChanged.connect(lambda: self.change_check_box())

        depth = uimthd.config_read('depth', 'depth')
        if depth:
            self.ui.depth.setCurrentText(depth)
        self.ui.depth.currentIndexChanged.connect(lambda: self.change_depth())

        self.ui.listview_result.doubleClicked.connect(self.clicked_list)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clt_timer)
        self.timer.start(3000)

        print("Initialization completed")

    def clt_timer(self):
        if self.task_scan_all_disk_part:
            if self.scan_state == 1 and not self.task_scan_all_disk_part.isAlive():
                self.scan_state = 0
                self.task_scan_all_disk_part = None
                with open(constant.ERROR_SCAN_LOG_FILE, 'r') as f:
                    self.ui.logTextArea.append(f.read())
                self.ui.logTextArea.append(utils.get_now_time("%Y-%m-%d %H:%M:%S") + " --扫描完毕--")
                self.ui.logTextArea.moveCursor(QTextCursor.End)
                uimthd.set_all_enabled(self.ui, True)
        if self.task_search:
            if self.search_state == 1 and not self.task_search.isAlive():
                self.search_state = 0
                self.task_search = None

    def scan_all_disk_part(self):
        """
        全盘扫描
        """
        self.ui.logTextArea.append(utils.get_now_time("%Y-%m-%d %H:%M:%S") + " --正在扫描磁盘，该过程时间较长--")
        self.scan_state = 1
        uimthd.set_all_enabled(self.ui, False)
        self.task_scan_all_disk_part = uimthd.scan_all_disk_part()

    def search(self):
        keyword = self.ui.queryEdit.text()
        depth = self.ui.depth.currentText()
        print('keyword', keyword)
        print('depth', depth)
        check, update_type, last_time, overdue, msg = uimthd.check_update_list(check_types=(0, 2))
        if check:
            if update_type == 0:
                reply = QMessageBox.question(self, "选择", msg, QMessageBox.Yes | QMessageBox.No)
                if reply == 65536:
                    pass
                else:
                    self.scan_all_disk_part()
                    return
            if update_type == 2:
                reply = QMessageBox.question(self, "选择", msg, QMessageBox.Yes | QMessageBox.No)
                if reply == 65536:
                    return
                else:
                    self.scan_all_disk_part()
                    return

        if not keyword:
            QMessageBox.information(self, "提示", "请输入关键字")
            return
        self.search_state = 1
        self.ui.logTextArea.append(utils.get_now_time("%Y-%m-%d %H:%M:%S") + ' 正在搜索"%s"' % keyword)
        self.ui.logTextArea.moveCursor(QTextCursor.End)
        checked_dist_part_list = []
        for _disk_part in dist_part_list:
            is_checked = eval("self.ui.checkBox_%s.isChecked()" % _disk_part)
            if is_checked:
                checked_dist_part_list.append(_disk_part)

        uimthd.set_all_enabled(self.ui, False)
        self.rst_lst.clear()
        slm = QStringListModel()
        slm.setStringList(self.rst_lst)
        self.ui.listview_result.setModel(slm)
        # search
        self.task_search = uimthd.search(self.ui, keyword, checked_dist_part_list, self.rst_lst)

    def change_check_box(self):
        ui = self.ui
        unchecked_list = []
        for _disk_part in dist_part_list:
            is_checked = eval("ui.checkBox_%s.isChecked()" % _disk_part)
            if not is_checked:
                unchecked_list.append(_disk_part)
        uimthd.save_checked_status(unchecked_list)

    def change_depth(self):
        uimthd.config_write("depth", "depth", self.ui.depth.currentText())

    def clicked_list(self, model_index):
        line = self.rst_lst[model_index.row()]
        if "：" in line:
            line = line[line.index('：') + 1:]
            cmd = 'explorer /select, "%s"' % line
            os.system(cmd)

    def init_check(self):
        check, update_type, last_time, overdue, msg = uimthd.check_update_list()
        if check:
            if update_type == 0:
                reply = QMessageBox.question(self, "选择", msg, QMessageBox.Yes | QMessageBox.No)
                if reply == 65536:
                    pass
                else:
                    self.scan_all_disk_part()
            elif update_type == 1:
                print("最后一次更新日期", last_time)
                print("过期时间", overdue)
                reply = QMessageBox.question(self, "选择", msg, QMessageBox.Yes | QMessageBox.No)
                if reply == 65536:
                    print('选择了No')
                    uimthd.config_write("user", "scan_next_day", (str(int(overdue) + 1)))
                else:
                    self.scan_all_disk_part()
            elif update_type == 2:
                reply = QMessageBox.question(self, "选择", msg, QMessageBox.Yes | QMessageBox.No)
                if reply == 65536:
                    pass
                else:
                    self.scan_all_disk_part()


if __name__ == '__main__':
    dist_part_list = []
    s_disk_part_iter = core.get_disk_info()
    for disk_part in s_disk_part_iter:
        if disk_part.fstype:
            dsk = disk_part.device[0:1]
            dist_part_list.append(dsk)
    print("Load disk information", dist_part_list)

    app = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    myDlg.init_check()
    sys.exit(app.exec_())
