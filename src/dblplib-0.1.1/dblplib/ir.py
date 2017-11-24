from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
import tempfile

fields = {'mdate': TEXT(stored=True),
    'key': ID,
    'title': TEXT(stored=True),
    'author': TEXT(stored=True),
    'editor': TEXT(stored=True),
    'year': TEXT(stored=True),
    'ee': TEXT(stored=True),
    'url': TEXT(stored=True),
    'crossref': TEXT(stored=True),
    'abstract': TEXT(stored=True),
    'note': TEXT(stored=True),
    'cdrom': TEXT(stored=True),
    'cite': TEXT(stored=True),
    'pages': TEXT(stored=True),
    'volume': TEXT(stored=True),
    'number': TEXT(stored=True),
    'journal': TEXT(stored=True),
    'publisher': TEXT(stored=True),
    'booktitle': TEXT(stored=True),
    'isbn': TEXT(stored=True),
    'series': TEXT(stored=True),
    'school': TEXT(stored=True),
    'type': TEXT(stored=True)}

schema = Schema(**fields)
indexdir = tempfile.mkdtemp()
ix = create_in(indexdir, schema)
writer = ix.writer()

def add_document(doc):
    return
    attrs = {}
    for attrname in fields.keys():
        if hasattr(doc, attrname) and doc.__getattribute__(attrname):
            attrs[attrname] = doc.__getattribute__(attrname)
    writer.add_document(**attrs)
    
def commit():
    return
    writer.commit()
