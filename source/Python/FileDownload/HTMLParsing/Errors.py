#!/usr/bin/python


class BadHTMLError(Exception):
    """
    Custom exception type for badly-formed HTML.
    """
    
    def __init__(self, message):
        super(type(self), self).__init__("Badly-formed HTML - " + message)

