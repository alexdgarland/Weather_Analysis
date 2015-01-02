#!/usr/bin/python


import sys
if sys.version_info[0] >= 3:
    from html.parser import HTMLParser
else:
    from HTMLParser import HTMLParser

import TagHandlingState as ths


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


class HTMLTableParser(HTMLParser, object):    
    """
    Parses HTML text into a nested list -
    each inner list represents a row in the table.
    
    The methods used to build the in-memory table structure
    are taken from a state machine (accessed via self._taghandlingstate)
    which transitions itself as the parser progresses through the document, 
    """

    def __init__(self):
        self._state_instances = { }
        super(type(self), self).__init__()
        
    def _transition(self, new_state_class):
        # Only act if handler function has returned a new state type
        if new_state_class:
            # Memoise reusable instances of state classes
            if new_state_class not in self._state_instances:
                self._state_instances[new_state_class] = new_state_class()
            # Assign instance to current state
            self._state = self._state_instances[new_state_class]
        
    def handle_starttag(self, tag, attrs):
        new_state = self._state.handle_starttag_state(tag, attrs, self._builder)
        self._transition(new_state)
        
    def handle_endtag(self, tag):
        new_state = self._state.handle_endtag_state(tag, self._builder)
        self._transition(new_state)

    def handle_data(self, data):
        new_state = self._state.handle_data_state(data, self._builder)
        self._transition(new_state)

    def handle_entityref(self, name):
        new_state = self._state.handle_entityref_state(name, self._builder)
        self._transition(new_state)

    def GetTable(self, html):
        self.feed(html)
        return self._builder.table

    def feed(self, html):
        self._builder = TableBuilder()
        self._transition(ths.DefaultTagHandlingState)
        super(type(self), self).feed(html) 

    