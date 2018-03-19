#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 21:33:49 2018

@author: wincrantu
"""


import zenhan as zh
import pandas as pd
from re import match


class GetClassroom:
    def __init__(self, today_datetime):
        self.nendo = today_datetime.year
        if today_datetime.month < 3:
            self.nendo -= 1

    def getClassroom(self, courseNo):
        courseNo = courseNo.replace("'", "")

        try:
            courseNo_int = int(courseNo)
            courseNo = "{:06%}".format(courseNo_int)
        except ValueError:
            return ""

        if not match(r"{0-9}[6]", courseNo):
            return ""

        obj_url = ("https://gs.okayama-u.ac.jp/campusweb/campussquare.do?_"
                   "flowId=SYW4101101-flow&nendo={nendo}&"
                   "shozoku={shozoku}&jikanwari={jikanwari}"
                   "&sylocale=ja_JP").format(nendo=self.nendo,
                                             shozoku=courseNo[0:2],
                                             jikanwari=courseNo[2:6])

        try:
            df = pd.read_html(obj_url)
        except ValueError:
            return ""

        return self.changeClassroom(df[0][1][6])

    def changeClassroom(self, classroom):
        if match(r".*,.*", classroom):
            cr = classroom
        elif classroom == "工学部１号館情報実習室１（CAE室）":
            cr = "工1-CAE室"
        elif match(r"一般教育棟.*", classroom):
            cr = classroom.replace("一般教育棟", "").replace("教室", "")
        elif match(r"工学部.*", classroom):
            cr = classroom.replace('工学部', "工").replace(
                "号館第", "-").replace("号館", "-").replace("講義室", "")
        elif match(r"情報実習室.*", classroom):
            cr = classroom.replace("情報実習室", "情")
        elif match(r"理学部.*", classroom):
            cr = classroom.replace("理学部", "理").replace(
                "号館第", "-").replace("号館", "-").replace("講義室", "")
        else:
            cr = classroom

        cr = cr.replace(" ", "")

        return zh.z2h(text=cr, mode=3)
