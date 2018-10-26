# -*- coding: UTF-8 -*-

class Record():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.organization = ""
        self.lab = ""
        self.first = []
        self.other = []

    def set_name(self, name):
        self.name = name

    def add_first(self, article):
        self.first.append(article)
    
    def rm_first(self, article):
        self.first.remove(article)

    def add_other(self, article):
        self.other.append(article)
    
    def rm_other(self, article):
        self.other.remove(article)