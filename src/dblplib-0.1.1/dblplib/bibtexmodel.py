
MODEL = { # This dict represents the bibtex model according to http://en.wikipedia.org/wiki/BibTeX
'article': {
'required': ('author', 'title', 'journal', 'year', 'key'),
'optional': ('volume', 'number', 'pages', 'month', 'note', 'abstract')
},

'book': {
'required': ('author', 'editor', 'title', 'publisher', 'year', 'key'),
'optional': ('volume', 'series', 'address', 'edition', 'month', 'note', 'abstract')
},
'booklet': {
'required': ('title', 'key'),
'optional': ('author', 'howpublished', 'address', 'month', 'year', 'note', 'abstract')
},

'inbook': {
'required': ('author', 'editor', 'title', 'chapter', 'pages', 'publisher', 'year', 'key'),
'optional': ('volume', 'series', 'address', 'edition', 'month', 'note', 'abstract')
},

'incollection': {
'required': ('author', 'title', 'booktitle', 'year', 'key'),
'optional': ('editor', 'pages', 'organization', 'publisher', 'address', 'month', 'note', 'abstract')
},

'inproceedings': {
'required': ('author', 'title', 'booktitle', 'year', 'key'),
'optional': ('editor', 'series', 'pages', 'organization', 'publisher', 'address', 'month', 'note', 'abstract')
},

'manual': {
'required': ('title', 'key'),
'optional': ('author', 'organization', 'address', 'edition', 'month', 'year', 'note', 'abstract')
},

'masterthesis': {
'required': ('author', 'title', 'school', 'year', 'key'),
'optional': ('address', 'month', 'note', 'abstract')
},

'misc': {
'required': ('key',),
'optional': ('author', 'title', 'howpublished', 'month', 'year', 'note', 'abstract')
},

'phdthesis': {
'required': ('author', 'title', 'school', 'year', 'key'),
'optional': ('address', 'month', 'note', 'abstract')
},

'proceedings': {
'required': ('title', 'year', 'key'),
'optional': ('editor', 'publisher', 'organization', 'address', 'month', 'note', 'abstract')
},

'techreport': {
'required': ('author', 'title', 'institution', 'year', 'key'),
'optional': ('techreport_type', 'number', 'address', 'month', 'note', 'abstract')
},

'unpublished': {
'required': ('author', 'title', 'note', 'key'),
'optional': ('month', 'year', 'abstract')
},
}

# Extract the fields from the MODEL dict
fields = []
for typename, fieldnames in MODEL.items():
    for k, names in fieldnames.items():
        fields.extend(names)
FIELDS = set(fields) # Unique fields

class Person(object):
    first_name = ''
    last_name = ''
    complete_name = ''
    
    def __unicode__(self):
        return self.complete_name

class Author(Person):
    def __init__(self):
        super(Author, self).__init__()

class Editor(Person):
    def __init__(self):
        super(Editor, self).__init__()

class Document(object):
    """
    This class represents an entry of the DBLP library. The fields of this class
    are dynamically inserted according to the FIELDS variable defined in this file. Thus,
    refers to this variable in order to understand the available fields.
    """
    def __init__(self, mdate='', key=''):
        for field in FIELDS:
            self.__setattr__(field, '')
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
