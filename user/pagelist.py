#encoding: utf-8

import math
import json

import gconf

class PageList(object):
    
    _default_page_size = gconf.PAGE_SIZE
    _max_page_select = 5

    @classmethod
    def create_pagelist(cls, pageNum, pageSize, totalNum):
        pageSize = int(pageSize) if str(pageSize).isdigit() else cls._default_page_size
        pageSize = cls._default_page_size if pageSize <= 5 or pageSize >= 100 else pageSize

        _max_page_num = int(math.ceil(totalNum * 1.0 / pageSize))

        pageNum = int(pageNum) if str(pageNum).isdigit() else 1
        pageNum = 1 if pageNum < 1 or pageNum > _max_page_num else pageNum
    
        _offset = (pageNum - 1) * pageSize

        _start_page_num = pageNum
        _end_page_num = pageNum
        for _page in range(1, cls._max_page_select):
            if _start_page_num > 1:
                _start_page_num -= 1
            if _end_page_num < _max_page_num:
                _end_page_num += 1

            if _end_page_num - _start_page_num + 1 >= cls._max_page_select:
                break

        return cls(pageNum, pageSize, totalNum, _max_page_num, _start_page_num, _end_page_num), _offset 

    def __init__(self, pageNum, pageSize, totalNum, maxPageNum, startPageNum, endPageNum):
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.totalNum = totalNum
        self.maxPageNum = maxPageNum
        self.startPageNum = startPageNum
        self.endPageNum = endPageNum

    def set_contents(self, contents=[]):
        self.contents = contents

    def __str__(self):
        return str(self.__dict__)