'''
Created on Dec 2, 2010

@author: yguarata
'''
import xml.parsers.expat
import HTMLParser
import codecs

unescape = HTMLParser.HTMLParser().unescape

class Person(object):
    first_name = None
    last_name = None
    complete_name = None
    
    def __unicode__(self):
        return self.complete_name

class Author(Person):
    def __init__(self):
        super(Author, self).__init__()

class Editor(Person):
    def __init__(self):
        super(Editor, self).__init__()

class Document(object):
    mdate = None
    key = None
    title = None
    year = None
    ee = None
    url = None
    crossref = None
    abstract = None
    
    def __init__(self, mdate=None, key=None):
        self.mdate = mdate
        self.key = key
        self.authors = []
        self.editors = []
        
    def __str__(self):
        s = "Key: %s\nTitle: %s\nYear: %s\nEE: %s\nURL: %s" % (self.key, self.title, 
                                                               self.year, self.ee, self.url)
        for i, a in enumerate(self.authors):
            s += '\nAuthor %d: %s' % (i+1, unicode(a))
        for i, e in enumerate(self.editors):
            s += '\nEditor %d: %s' % (i+1, unicode(e))
            
        return s
    
class Article(Document):
    pages = []
    volume = None
    number = None
    journal = None
    publisher = None
    
    def __init__(self, mdate=None, key=None):
        super(Article, self).__init__(mdate, key)
        
    def __str__(self):
        s = "\n-- Article --\n" + super(Article, self).__str__()
        if self.pages:
            s += "\nPages: %s-%s" % (self.pages[0], self.pages[1])
        s += "\nVolume: %s" % self.volume
        s += "\nNumber: %s" % self.number
        s += "\nJournal: %s" % self.journal
        s += "\nPublisher: %s" % self.publisher
        return s

class Proceedings(Document):
    booktitle = None
    volume = None
    isbn = None
    series = None
    publisher = None
    
    def __init__(self, mdate=None, key=None):
        super(Proceedings, self).__init__(mdate, key)
        
    def __str__(self):
        s = "\n-- Proceedings --\n" + super(Proceedings, self).__str__()
        s += "\nTitle: %s" % self.title
        s += "\nBook title: %s" % self.booktitle
        s += "\nISBN: %s" % self.isbn
        s += "\nSeries: %s" % self.series
        s += "\nPublisher: %s" % self.publisher
        return s

class InProceedings(Proceedings):
    pages = []
    
    def __init__(self, mdate=None, key=None):
        super(InProceedings, self).__init__(mdate, key)
        
    def __str__(self):
        s = "\n-- In Proceedings --\n" + super(InProceedings, self).__str__()
        s += "\nBook title: %s" % self.booktitle
        if self.pages:
            s += "\nPages: %s-%s" % (self.pages[0], self.pages[1])
        return s

class InCollection(Document):
    pages = []
    booktitle = None
    
    def __init__(self, mdate=None, key=None):
        super(InCollection, self).__init__(mdate, key)
        
    def __str__(self):
        s = "\n-- In Collection --\n" + super(InCollection, self).__str__()
        s += "\nBook title: %s" % self.booktitle
        return s

class Book(Document):
    isbn = None
    publisher = None
    
    def __init__(self, mdate=None, key=None):
        super(Book, self).__init__(mdate, key)
        
    def __str__(self):
        s = "\n-- Book --\n" + super(Book, self).__str__()
        s += "\nISBN: %s" % self.isbn
        s += "\nPublisher: %s" % self.publisher
        return s

class MastersThesis(Document):
    school = None
    
    def __init__(self, mdate=None, key=None):
        super(MastersThesis, self).__init__(mdate, key)
        
    def __str__(self):
        s = "\n-- Master thesis --\n" + super(MastersThesis, self).__str__()
        s += "\nSchool: %s" % self.school
        return s

class PhdThesis(MastersThesis):
    def __init__(self, mdate=None, key=None):
        super(PhdThesis, self).__init__(mdate, key)
        
    def __str__(self):
        s = "\n-- PhD thesis --\n" + super(PhdThesis, self).__str__()
        s += "\nSchool: %s" % self.school
        return s

class DBLPXMLParser:
    
    def __init__(self):
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.CharacterDataHandler = self.handleCharData
        self.parser.StartElementHandler = self.handleStartElement
        self.parser.EndElementHandler = self.handleEndElement
        self.documents = []
        self.doc_temp = None
        self.chars = ''
    
    def parse(self, xml_content):
        self.xml_content = unescape(xml_content).encode('utf-8')
        self.parser.Parse(self.xml_content, 1)
        return self.documents
    
    def handleCharData(self, data):
        self.chars = data
    
    def handleStartElement(self, name, attrs):
        if not name:
            return
        
        name = name.lower()
        
        if name == "article":
            self.doc_temp = Article(attrs['mdate'], attrs['key'])
        elif name == "inproceedings":
            self.doc_temp = InProceedings(attrs['mdate'], attrs['key'])
        elif name == "proceedings":
            self.doc_temp = Proceedings(attrs['mdate'], attrs['key'])
        elif name == "mastersthesis":
            self.doc_temp = MastersThesis(attrs['mdate'], attrs['key'])
        elif name == "phdthesis":
            self.doc_temp = PhdThesis(attrs['mdate'], attrs['key'])
        elif name == "book":
            self.doc_temp = Book(attrs['mdate'], attrs['key'])
        elif name == "incollection":
            self.doc_temp = InCollection(attrs['mdate'], attrs['key'])
        else:
            return
        
        self.documents.append(self.doc_temp)
            
    
    def handleEndElement(self, name):
        if not name or not self.doc_temp:
            return
        
        name = name.lower()
        
        if name == "author":
            author = Author()
            author.complete_name = self.chars
            self.doc_temp.authors.append(author)
        
        elif name == "editor":
            editor = Editor()
            editor.complete_name = self.chars
            self.doc_temp.editors.append(editor)
        
        elif name == "title":
            self.doc_temp.title = self.chars
        
        elif name == "crossref":
            self.doc_temp.crossref = self.chars
            
        elif name == "pages":
            if '-' in self.chars:
                self.doc_temp.pages = self.chars.split('-')
                
        elif name == "year":
            self.doc_temp.year = self.chars
            
        elif name == "volume":
            if '-' in self.chars:
                self.doc_temp.volume = self.chars.split('-')[0]
                self.doc_temp.number = self.chars.split('-')[1]
            else:
                self.doc_temp.volume = self.chars
        
        elif name == "number":
            if not '-' in self.chars:
                self.doc_temp.number = self.chars
            
        elif name == "ee":
            self.doc_temp.ee = self.chars
            
        elif name == "url":
            self.doc_temp.url = self.chars
            
        elif name == "series":
            self.doc_temp.series = self.chars
            
        elif name == "isbn":
            self.doc_temp.isbn = self.chars
            
        elif name == "publisher":
            self.doc_temp.publisher = self.chars
            
        elif name == "school":
            self.doc_temp.school = self.chars
            
        elif name == "booktitle":
            self.doc_temp.booktitle = self.chars
            
        elif name == "journal":
            self.doc_temp.journal = self.chars
            
        else:
            print 'Skiped end tag:', name
