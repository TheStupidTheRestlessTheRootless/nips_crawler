# -*- coding: UTF-8 -*-
import json
from tools import serialize_instance

class Record():
    def __init__(self, id):
        self.id = id
        self.name = ""
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

    def toJSON(self):
        return json.dumps(self, default=serialize_instance)


class Poster():
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def toJSON(self):
        return json.dumps(self, default=serialize_instance)