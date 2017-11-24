# Graph Aggregator for DBLP Dataset
Repository containing scripts used during the development of prototype for my Master's Project. The dissertation explaning all the research behind it can be found [here](https://github.com/nicysneiros/dissertation).

### Dependencies
To run these scripts, you will need to have installed:

- [Python 2.7](https://www.python.org/downloads/)
- [Virtual Env Wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)

Once those are installed, create a new virtual environment for the project using the terminal:
```
mkvirtualenv dblp
```

Now, you'll need to install the depencencies by running the following command inside `src` directory:
```
make deps
```

### Running Scripts
1. In `load_dblp.py`:

	- Specify your SQLite connection string.
	- Setup your Neo4J connection information.
	- Remember to download the DBLP dataset from here: [http://dblp.uni-trier.de/xml/](http://dblp.uni-trier.de/xml/)

2. Run `load_dblp.py` to parse all the entries in `dblp.xml` to a SQLite DB and then load it to Neo4J.

	- The part to parse the data from the XML file may take a while :cry:. Go get a drink or go to sleep (that's what I did :sleeping:).
	- You only need to parse from `dblp.xml` once... you can comment the line 19 once you have your SQLite DB populated.
	- In this script you can tweak what date you actually want to have in Neo4J. For instance, I created a view to select just a subset of the original DBLP data.

3. Run `graph_aggregator.py` once your Neo4J DB is populated. This script is used to generate the Aggregated Graph that allows us to perform OLAP queries in the graph DB. Make sure to change the `dimensions` list accordingly.

4. Now that your Aggregated Graph is up and running, you can submit your OLAP queries in it :information_desk_person:.

### Trick or Treats
In order to run the `graph_aggregator.py` script, you'll need two instances of Neo4J running at the same time. I was able to accomplish that by using a Neo4J Instance Manager called [iNeo](https://github.com/cohesivestack/ineo).
