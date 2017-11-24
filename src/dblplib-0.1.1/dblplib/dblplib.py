'''
Created on Mar, 2014

A Python lib to parse the DBLP Computer Science Bibliography. It provides a 
class model which is used to extract publication entries from the XML file 
provided by the DBLP.
'''
import xml.parsers.expat
import HTMLParser
import ir
import db
from StringIO import StringIO
from bibtexmodel import *
from parser import DBLPXMLParser

unescape = HTMLParser.HTMLParser().unescape

def parse_file(path, *args, **kargs):
    """Parses the file pointed by 'path' containing the DBLP bibtex entries 
    and stores the entries."""
    print 'Parsing %s...' % path
    DBLPXMLParser(*args, **kargs).parse_file(open(path, 'r'))
    
def parse(xml_content, *args, **kargs):
    """Parses the 'xml_content' containing the DBLP bibtex entries 
    and stores the entries."""
    DBLPXMLParser(*args, **kargs).parse(xml_content)

def search(*args, **kargs):
    """
    Search entries by performin an exact match. You must pass key-value pairs 
    according to the following accepted keys: 'series', 'abstract', 'number', 'month', 
    'edition', 'year', 'techreport_type', 'title', 'booktitle', 'institution', 'note', 
    'editor', 'howpublished', 'journal', 'volume', 'key', 'address', 'pages', 'chapter',
    'publisher', 'school', 'author', 'organization'

    It returns a SQLAlchemy query which contains objects of bibtexmodel.Document.
    """
    return db.search(*args, **kargs)

def insert(document):
    """
    Inserts a new entry to the storage. 
    The document argument must be an object of bibtexmodel.Document.
    """
    db.insert(document)

def get(key, *args, **kargs):
    """Returns an entry specified by its key. The return is an object of bibtexmodel.Document"""
    return db.get(key)

def delete(key, *args, **kargs):
    """Delete an entry according to the given key."""
    db.delete(key)

def delete_all():
    db.delete_all()

def count():
    """Returns the number of entries stored."""
    return db.count()

