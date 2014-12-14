#!/usr/bin/python
from abc import ABCMeta, abstractmethod
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

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
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
        if tag == 'th':
            self.transition_to(HeaderTagHandlingState)
        elif tag == 'tr':
            self.transition_to(RowTagHandlingState)
        
    def handle_endtag(self, tag):
        if tag == 'table':
            if self._parser.has_open_row():
                # Raise error - could just commit row if we want to handle tolerantly
                raise Exception("Badly-formed HTML - table ends without completing open row.")
            self.transition_to(DefaultTagHandlingState)


class RowTagHandlingState(AbstractTagHandlingState):
    """
    Processes stuff... :-)
        **** TO DO ****
    """
    def handle_starttag(self, tag, attrs):
        # Here's where we actually do some stuff
        pass
    
    def handle_endtag(self, tag, activetag='tr'):
        if tag == activetag:
            self._parser.commit_row()
            self.transition_to(TableTagHandlingState)


class HeaderTagHandlingState(RowTagHandlingState):
    
    def handle_starttag(self, tag, attrs):
        # Here's where we actually do some stuff
        pass
    
    def handle_endtag(self, tag):
        super(type(self), self).handle_endtag(tag, activetag='th')


# Also probably need cell and link handling states

# The parser itself:

class HTMLTableParser(HTMLParser):

    def set_state(self, newstate):
        self._taghandlingstate = newstate(parser=self)
    
    def has_open_row(self):
        return (self._currentrow != [])
    
    def commit_row(self):
        self._table.append(self._currentrow)
        self._currentrow = []
        
    def commit_link(self):
        self._currentrow.append(self._currentlink)
        self._currentlink = {}
    
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

    def GetTable(self, html):
        """
        Parse the HTML table to a nested list as a simple first step,
        from which we can later identify file info through further processing.
        """
        self.feed(html)
        return self._table
