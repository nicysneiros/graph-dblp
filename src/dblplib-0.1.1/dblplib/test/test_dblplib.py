from dblplib import parse, parse_file
import dblplib
from bibtexmodel import Document
import db
import unittest
import os
import codecs
import tempfile
import HTMLParser

unescape = HTMLParser.HTMLParser().unescape

testXML = u"""<?xml version="1.0" encoding="ISO-8859-1"?>
    <dblp>
    <article key="journals/cacm/Szalay08" mdate="2008-11-03">
        <author>Alexander S. Szalay</author>
        <author>Yguarata Cerqueira Cavalcanti</author>
        <author>Antonio Carlos Jose da Silva</author>
        <title>Jim Gray, astronomer.</title>
        <pages>58-65</pages>
        <year>2008</year>
        <volume>51</volume>
        <journal>Commun. ACM</journal>
        <number>11</number>
        <ee>http://doi.acm.org/10.1145/1400214.1400231</ee>
        <url>db/journals/cacm/cacm51.html#Szalay08</url>
    </article>
    <incollection mdate="2013-09-10" key="series/cogtech/SchmitzBNSS13">
		<author>Michael Schmitz</author>
		<author>Boris Brandherm</author>
		<author>Jorg Neidig</author>
		<author>Stefanie Schachtl</author>
		<author>Matthias Schuster</author>
		<title>Interaction Modalities for Digital Product Memories.</title>
		<pages>261-279</pages>
		<year>2013</year>
		<booktitle>SemProM</booktitle>
		<ee>http://dx.doi.org/10.1007/978-3-642-37377-0_16</ee>
		<crossref>series/cogtech/364237376</crossref>
		<url>db/series/cogtech/364237376.html#SchmitzBNSS13</url>
	</incollection>
	<incollection mdate="2013-09-10" key="series/cogtech/HayashiDCMSB11">
		<author>Yoshihiko Hayashi</author>
		<author>Thierry Declerck</author>
		<author>Nicoletta Calzolari</author>
		<author>Monica Monachini</author>
		<author>Claudia Soria</author>
		<author>Paul Buitelaar</author>
		<title>Language Service Ontology.</title>
		<pages>85-100</pages>
		<year>2011</year>
		<booktitle>The Language Grid</booktitle>
		<ee>http://dx.doi.org/10.1007/978-3-642-21178-2_6</ee>
		<crossref>series/cogtech/364221177</crossref>
		<url>db/series/cogtech/364221177.html#HayashiDCMSB11</url>
	</incollection>
	<incollection mdate="2013-09-10" key="series/cogtech/JamesonKMGWR11">
		<author>Anthony Jameson</author>
		<author>Juergen Kiefer</author>
		<author>Christian A. Muller</author>
		<author>Barbara Gromann-Hutter</author>
		<author>Frank Wittig</author>
		<author>Ralf Rummer</author>
		<title>Assessment of a User's Time Pressure and Cognitive Load on the Basis of Features of Speech.</title>
		<pages>171-204</pages>
		<year>2011</year>
		<booktitle>Resource-Adaptive Cognitive Processes</booktitle>
		<ee>http://dx.doi.org/10.1007/978-3-540-89408-7_9</ee>
		<crossref>series/cogtech/354089408</crossref>
		<url>db/series/cogtech/354089408.html#JamesonKMGWR11</url>
	</incollection>
	<incollection mdate="2013-09-10" key="series/cogtech/LinK12">
		<author>Raz Lin</author>
		<author>Sarit Kraus</author>
		<title>From Research to Practice: Automated Negotiations with People.</title>
		<pages>195-212</pages>
		<year>2012</year>
		<booktitle>Ubiquitous Display Environments</booktitle>
		<ee>http://dx.doi.org/10.1007/978-3-642-27663-7_12</ee>
		<crossref>series/cogtech/364227662</crossref>
		<url>db/series/cogtech/364227662.html#LinK12</url>
	</incollection>
	</dblp>"""

TOTAL_ENTRIES = 5

class DBLPLibTest(unittest.TestCase):

    def setUp(self):
        db.delete_all()

    def test_parse(self):
        parse(testXML)
        self.assertTrue(db.count() > 0)

    def test_parse_file(self):
        f = tempfile.NamedTemporaryFile(delete=False);
        f.write(unescape(testXML).encode('utf-8'));
        f.close()
        parse_file(f.name)
        os.unlink(f.name)
        self.assertTrue(dblplib.count() > 0)

    def test_parsed_entries(self):
        parse(testXML)
        key = "series/cogtech/LinK12"
        doc = dblplib.get(key)
        self.assertEqual(key, doc.key)

        key = "not exists"
        self.assertEqual(None, dblplib.get(key))

    def test_search(self):
        parse(testXML)
        self.assertTrue(dblplib.search(key="series/cogtech/LinK12", count=True) > 0)

    def test_delete(self):
        parse(testXML)
        key = "series/cogtech/LinK12"
        doc = dblplib.get(key)
        self.assertEqual(key, doc.key)
        dblplib.delete(doc.key)
        self.assertRaises(Exception, dblplib.get(key))

if __name__ == '__main__':
    unittest.main()
