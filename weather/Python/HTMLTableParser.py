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
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def handle_start_tag(self, parser):
        pass
    @abstractmethod
    def handle_end_tag(self, parser):
        pass
    @abstractmethod
    def handle_data(self, parser):
        pass

#class DefaultTagHandlingState()




# The parser itself:

class HTMLTableParser(HTMLParser):
    
    def feed(self):
        self._table = None
        self._taghandlingstate = DefaultTagHandlingState()
        super(type(self)).feed()
        
    def GetTable(self, html):
        """
        Parse the HTML table to a nested list as a simple first step,
        from which we can later identify file info through further processing.
        """
        self.feed()
        return self._table
