#!/usr/bin/python


class TableBuilder(object):
    """
    Class to build in-memory (nested list) representation of table from HTML.
    """
    
    def __init__(self):
        self.table = []
        self.currentrow = []
        self.currentlink = {}

    def __iter__(self):
        return self.table.__iter__()

    def add_cell(self, celldata):
        self.currentrow.append(celldata)
        
    def commit_link(self):
        self.add_cell(self.currentlink)
        self.currentlink = {}
        
    def commit_row(self):
        if self.currentrow != []:
            self.table.append(self.currentrow)
            self.currentrow = []

