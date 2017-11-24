from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker, mapper
from bibtexmodel import FIELDS, Document


class DB:
    def __init__(self, *args, **kwargs):
        db_conn_str = kwargs.get('db_conn_str')

        if db_conn_str:
            self.engine = create_engine(db_conn_str)
        else:
            self.engine = create_engine('sqlite:///:memory:', echo=True)

        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()
        self.metadata = MetaData(bind=self.engine)

        # Create the database
        fields = [Column('key', String(255), primary_key=True)]

        for field in FIELDS:
            if field == 'key':
                continue
            fields.append(Column(field, String(255)))

        document_table = Table('bibtex_entry', self.metadata, *fields)
        mapper(Document, document_table)
        self.metadata.create_all(self.engine)

    def search(self, *args, **kargs):
        if kargs.has_key('page'):
            page = kargs['page']
            del kargs['page']
        if kargs.has_key('amount_per_page'):
            amount = kargs['amount_per_page']
            del kargs['amount_per_page']
        if kargs.has_key('count'):
            count = kargs['count']
            del kargs['count']

        results = self.session.query(Document).filter_by(**kargs)

        if count:
            return results.count()

        if amount:
            results = results.limit(amount)
        if page:
            results = results.offset(page * amount)

        return results

    def insert(self, document):
        """Inserts a new entry to the storage."""
        entry = Document()
        for field in FIELDS:
            if hasattr(document, field):
                entry.__setattr__(field, document.__getattribute__(field))
            else:
                entry.__setattr__(field, '')
        self.session.add(entry)
        self.session.commit()

    def get(self, key, *args, **kargs):
        """Returns an entry according to the given key."""
        results = self.session.query(Document).filter(Document.key == key)
        if results.count() > 0:
            return results[0]
        else:
            return None

    def delete(self, key, *args, **kargs):
        """Delete an entry according to the given key."""
        results = self.session.query(Document).filter(Document.key == key)
        if results.count() > 0:
            self.session.delete(results[0])
            self.session.commit()
        else:
            raise Exception('There is no entry with key = ' + key + '.')

    def delete_all(self):
        for d in self.session.query(Document).all():
            self.session.delete(d)
        self.session.commit()

    def count(self):
        """Returns the number of entries stored."""
        return self.session.query(Document).count()
