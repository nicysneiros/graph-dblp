# -*- coding: utf-8 -*-
from dblplib.dblplib import parse_file
from dblplib.bibtexmodel import Document
from dblplib import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from py2neo import Graph, Node, Relationship, NodeSelector
from py2neo.packages.httpstream import http
from random import randint

http.socket_timeout = 9999
months = [
    'January', 'February', 'March',
    'April', 'May', 'June',
    'July', 'August', 'September',
    'October', 'November', 'December']

db_conn_str = 'sqlite:////Users/nicolle/Documents/UFPE/Mestrado/DBLPApp/src/sqlite_db/dblp.db'
parse_file('../dblp.xml', db_conn_str=db_conn_str)
engine = create_engine(db_conn_str)
conn = engine.connect()

g = Graph(http_port=7476, password="admin")
selector = NodeSelector(g)

results = conn.execute('SELECT * FROM main_publications')
i = 0

for doc in results:
    i += 1
    print "hello"
    tx = g.begin()

    publication = {
        'key': doc.key,
        'title': doc.title,
        'year': doc.year,
        'month': months[randint(0, 11)],
        'journal': doc.key.split('/')[1]
    }

    pub_node = Node('Publication', **publication)
    tx.create(pub_node)

    if hasattr(doc, 'author'):
        authors = [author.strip() for author in doc.author.split(",")]
        authors_nodes = []
        for author in authors:
            existing_author_node = selector.select('Author', name=author).first()
            if existing_author_node:
                author_node = existing_author_node
            else:
                author_node = Node('Author', name=author)
                tx.create(author_node)

            authors_nodes.append(author_node)
            published_rel = Relationship(
                author_node,
                "PUBLISHED",
                pub_node
            )
            tx.create(published_rel)

        for author_node in authors_nodes:
            for other_author in authors_nodes:
                if not other_author == author_node:
                    co_authorship_rel = g.match(
                        start_node=author_node, 
                        rel_type="CO_AUTHORSHIP",
                        end_node=other_author,
                        bidirectional=True)

                    co_authorship_rel_list = list(co_authorship_rel)
                    if len(co_authorship_rel_list) == 0:  # Relationship does not exist
                        new_co_authorship_rel = Relationship(
                            author_node,
                            "CO_AUTHORSHIP",
                            other_author,
                            count=1)
                        tx.create(new_co_authorship_rel)

    tx.commit()
    print i, " publication(s) created"
print ""