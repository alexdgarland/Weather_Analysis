#!/usr/bin/python


from abc import ABCMeta


class BadHTMLError(Exception):
    """
    Custom exception type for badly-formed HTML.
    """
    
    def __init__(self, message):
        super(type(self), self).__init__("Badly-formed HTML - " + message)


# Set up various tag handlers which will be used
# as part of a state machine within module HTMLTableParser.

class AbstractTagHandlingState(object):
    """
    Abstract class defining required methods for tag handling states.
    In their default implementation they do nothing;
    at least one method should be overridden for any concrete inheriting class.
    """

    # Python-2-style abstract class.
    # If done this way, class can technically be instantiated
    # if run in Python 3 interpreter
    # but alternative (Py3 syntax) won't work in Py2 at all.
    __metaclass__ = ABCMeta        
    
    def handle_starttag_state(self, tag, attrs, tablebuilder):
        pass

    def handle_data_state(self, data, tablebuilder):
        pass

    def handle_entityref_state(self, name, tablebuilder):
        pass

    def handle_endtag_state(self, tag, tablebuilder):
        pass


class DefaultTagHandlingState(AbstractTagHandlingState):
    """
    Starting state for HTML parsing, in this state nothing is added
    to the table construct, but it will handle transition
    to more active states where required.
    """

    def handle_starttag_state(self, tag, attrs, tablebuilder):
        if tag == 'table':
            return TableTagHandlingState


class TableTagHandlingState(AbstractTagHandlingState):
    """
    Basically just acts to transition into row handling state.
    """

    def handle_starttag_state(self, tag, attrs, tablebuilder):
        if tag == 'tr':
            return RowTagHandlingState
        
    def handle_endtag_state(self, tag, tablebuilder):
        if tag in ('body', 'html'):
            raise BadHTMLError("Document ends without closing table.")
        else:
            return DefaultTagHandlingState


class RowTagHandlingState(AbstractTagHandlingState):
    """
    Handles transitions in and out of cell handling states.
    """

    def handle_starttag_state(self, tag, attrs, tablebuilder):
        if tag == 'th':
            return HeaderCellTagHandlingState
        elif tag == 'td':
            return DataCellTagHandlingState
        
    def handle_endtag_state(self, tag, tablebuilder):
        if tag == 'table':
            raise BadHTMLError("Table ends without closing row.")        
        if tag in ('body', 'html'):
            raise BadHTMLError("Document ends without closing row.")
        if tag == 'tr':
            tablebuilder.commit_row()
            return TableTagHandlingState


class AbstractCellTagHandlingState(AbstractTagHandlingState):
    """
    Abstract base class holding shared processing functionality
    for two types of cells (header, data).
    """
    
    # Python-2-style abstract class.
    # If done this way, class can technically be instantiated
    # if run in Python 3 interpreter
    # but alternative (Py3 syntax) won't work in Py2 at all.
    __metaclass__ = ABCMeta
    
    def handle_data_state(self, data, tablebuilder):
        # Append text content to list for current row.
        tablebuilder.add_cell(data.strip())

    def handle_entityref_state(self, name, tablebuilder):
        if name == 'nbsp':
            tablebuilder.add_cell('')
    

class HeaderCellTagHandlingState(AbstractCellTagHandlingState):
    """
    Handles transition back to row handling state.
    We use only the processing from the abstract base class
    (i.e., we are not interested in links in the header).
    """

    def handle_endtag_state(self, tag, tablebuilder):
        if tag == 'th':
            return RowTagHandlingState


class DataCellTagHandlingState(AbstractCellTagHandlingState):
    """    
    Handles transition back to row handling state (as per the header state).
    Also adds processing logic and an onward state transition to handle links.
    """

    def handle_starttag_state(self, tag, attrs, tablebuilder):
        if tag == 'a':
            if len(attrs) >= 1 and attrs[0][0] == 'href':
                tablebuilder.currentlink['href'] = attrs[0][1]
            return LinkTagHandlingState

    def handle_endtag_state(self, tag, tablebuilder):
        if tag == 'td':
            return RowTagHandlingState
            

class LinkTagHandlingState(AbstractTagHandlingState):
    """
    Adds the text content of the cell to the current link dictionary
    which will already have an href added by the cell handler state.
    On exiting the state, adds the link (dict) to the current row
    and returns to the cell handler state.
    """
    
    def handle_data_state(self, data, tablebuilder):
        tablebuilder.currentlink['text'] = data.strip()

    def handle_endtag_state(self, tag, tablebuilder):
        if tag == 'a':
            tablebuilder.commit_link()
            return DataCellTagHandlingState

