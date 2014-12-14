#!/usr/bin/python

from abc import ABCMeta
import sys
if sys.version_info.major >= 3:
    from html.parser import HTMLParser
else:
    from HTMLParser import HTMLParser


# Set up various tag handlers which will be used
# as part of a state machine within the parser.


class AbstractTagHandlingState(object):
    """
    Abstract class defining required methods for tag handling states.
    In their default implementation they do nothing;
    at least one method should be overridden for any concrete inheriting class.
    """
    __metaclass__ = ABCMeta
    
    def __init__(self, parser):
        self._parser = parser
        
    def transition_to(self, newstate):
        self._parser.set_state(newstate)
    
    def handle_starttag(self, tag, attrs):
        pass

    def handle_data(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_endtag(self, tag):
        pass



class DefaultTagHandlingState(AbstractTagHandlingState):
    """
    Starting state for HTML parsing, in this state nothing is added
    to the table construct, but it will handle transition
    to more active states where required.
    """
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.transition_to(TableTagHandlingState)


class TableTagHandlingState(AbstractTagHandlingState):
    """
    Basically just acts to transition into row handling state.
    """
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.transition_to(RowTagHandlingState)
        
    def handle_endtag(self, tag):
        if tag == 'table':
            if self._parser.has_open_row():
                # Raise error - could just commit row
                # if we want to handle tolerantly
                raise Exception("Badly-formed HTML - " +
                                "table ends without completing open row.")
            else:
                self.transition_to(DefaultTagHandlingState)


class RowTagHandlingState(AbstractTagHandlingState):

    def handle_starttag(self, tag, attrs):
        if tag == 'th':
            self.transition_to(HeaderCellTagHandlingState)
        elif tag == 'td':
            self.transition_to(DataCellTagHandlingState)
        
    def handle_endtag(self, tag):
        if tag == 'tr':
            self._parser.commit_row()
            self.transition_to(TableTagHandlingState)


class HeaderCellTagHandlingState(AbstractTagHandlingState):
    # Note that unlike with data cells, we are not interested
    # in any link attributes present in start tags.

    def handle_data(self, data):
        # Append text content to list for current row.
        self._parser.add_cell(data.strip())

    def handle_entityref(self, name):
        if name == 'nbsp':
            self._parser.add_cell('')

    def handle_endtag(self, tag):
        if tag == 'th':
            self.transition_to(RowTagHandlingState)


class DataCellTagHandlingState(AbstractTagHandlingState):
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if len(attrs) >= 1 and attrs[0][0] == 'href':
                self._parser._currentlink['href'] = attrs[0][1]
            self.transition_to(LinkTagHandlingState)
    
    def handle_data(self, data):
        self._parser.add_cell(data.strip())
        
    def handle_entityref(self, name):
        if name == 'nbsp':
            self._parser.add_cell('')

    def handle_endtag(self, tag):
        if tag == 'td':
            self.transition_to(RowTagHandlingState)
            
            
## TO DO: header and data cells share a lot of functionality
## so can refactor to inherit from shared base class once they pass tests.


class LinkTagHandlingState(AbstractTagHandlingState):
    
    def handle_data(self, data):
        self._parser._currentlink['text'] = data.strip()

    def handle_endtag(self, tag):
        if tag == 'a':
            self._parser.commit_link()
            self.transition_to(DataCellTagHandlingState)


class HTMLTableParser(HTMLParser):    
    """
    Parses HTML text into a nested list -
    each inner list represents a row in the table.
    """    
    
    def set_state(self, newstate):
        self._taghandlingstate = newstate(parser=self)
    
    def has_open_row(self):
        return (self._currentrow != [])
            
    def add_cell(self, celldata):
        self._currentrow.append(celldata)

    def commit_link(self):
        self.add_cell(self._currentlink)
        self._currentlink = {}
    
    def commit_row(self):
        if self.has_open_row():
            self._table.append(self._currentrow)
            self._currentrow = []
        
    def feed(self, html):
        self._table = []
        self._currentrow = []
        self._currentlink = {}
        self.set_state(DefaultTagHandlingState)
        super(type(self), self).feed(html)        
        
    def handle_starttag(self, tag, attrs):
        self._taghandlingstate.handle_starttag(tag, attrs)
        
    def handle_endtag(self, tag):
        self._taghandlingstate.handle_endtag(tag)

    def handle_data(self, data):
        self._taghandlingstate.handle_data(data)

    def handle_entityref(self, name):
        self._taghandlingstate.handle_entityref(name)

    def GetTable(self, html):
        self.feed(html)
        return self._table
