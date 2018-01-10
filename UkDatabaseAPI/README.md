UkDatabaseAPI
========================

The "UkDatabaseAPI" is created to provide developers with a tool to search by criteria the scraped information.

Requirements
------------

  * Python 3 or higher;
  * MongoDB;
  * nltk;
  * bson;
  * pymongo;
  * Flask;
  * requests;
  
If unsure about meeting these requirements, download the API and
browse the [Flask](http://flask.pocoo.org/docs/0.12), [MongoDB](https://docs.mongodb.com)
and [PyMongo](https://api.mongodb.com/python/current)
documentation to get more detailed information.

Installation
------------

First, install [Python 3](https://www.python.org) and [MongoDB](https://www.mongodb.com)
if you haven't already. Then, install Flask, pymongo, nltk, bson and requests by executing
these commands anywhere in your system:

```terminal
$ pip install flask
```

```terminal
$ pip install pymongo
```

```terminal
$ pip install nltk
```

```terminal
$ pip install bson
```

```terminal
$ pip install requests
```

If the `pip` command is not available, update your package manager to the
most recent version executing the  
`python -m pip install --upgrade pip` (Windows) command.

Usage
-----

First start the `mongod.exe` from `~\MongoDB\Server\3.6\bin` or just type 
`mongod` in the command prompt (if а path to the bin folder is available).
Then open the command prompt (terminal) from the project folder 
and type the following command:
```terminal
$ python app.py
```
**Execute these commands anywhere in your system to create a text index:**
```terminal
$ mongo
$ use UkDatabase
$ db.posts.createIndex({TEXT: "text"})
```
**Without a text index you won't be able to make text searches.**

Open your browser and go to [http://localhost:5000/](http://localhost:5000)

**The API code allows to be deployed directly to [Heroku](https://www.heroku.com).***

*Before deploying the API change the MongoDB URI to your preference. 
(`~\UkDatabaseAPI\UkDatabaseAPI\database\mongo_db.py`)

```python
MONGO_URI = "mongodb://localhost:27017"
```

### How to work with the API


To find information about a person or an article use: [http://localhost:5000/search](http://localhost:5000/search).
You can make a search request by three criteria:
  
* Text;
* The post published date;
* Number of returned results;

Search by text, examples:

* http://localhost:5000/search?t=tom
* http://localhost:5000/search?t=sexual%20abuse

Search by date, examples:

* Posts published on a specific date:
    * http://localhost:5000/search?d=31/12/2017
* Posts from the first published post until a specific date:
    * http://localhost:5000/search?d=-31/12/2017
* Posts from a specific date until the last published post:
    * http://localhost:5000/search?d=31/12/2017-
* Posts within a time range (20/12/2017-31/12/2017):
    * http://localhost:5000/search?d=20/12/2017-31/12/2017

Limit the number of returned results, example:
* http://localhost:5000/search?t=tom%20from%20london&n_results=2

Of course you can combine the three criteria:
* http://localhost:5000/search?t=john%20from%20london&d=01/01/2018-&n_results=1

Result example:

URL:  
http://localhost:5000/search?t=John%20Bancroft%20dropped%20his%20son%20off&d=30/12/2017&n_results=1

Result:  
[{"_id": {"$oid": "5a4bc55586f8b4200864c476"}, 
"TITLE": "Michael Cohen \u2013\u00a0Portslade", 
"TEXT": "December 2017 Sale...", 
"POST_PUB_DATE": {"$date": 1514592000000}, 
"IMAGES": ["https://chrisukorg.files.wordpress.com/2017/12/cohen.jpg?w=529&h=352"], 
"score": 2.2608303249097474}]
 
The score is based on matching the searched text with the 
text in the article. The returned results are sorted in **descending**
order by the score.

Troubleshooting
---------------

If you get problems creating index in MongoDB or you get
these errors (run the following commands in the command prompt):

* `key too large to index`
    ```terminal
    $ mongod --setParameter failIndexKeyTooLong=false
    ```
* `text index required for $text query`
    ```terminal
    $ mongo
    $ use UkDatabase
    $ db.posts.createIndex({TEXT: "text"})
    ```
For more information see [MongoDB Text Index documentation](https://docs.mongodb.com/manual/core/index-text).

If you still can't fix this problem go to 
`~\UkDatabaseAPI\UkDatabaseAPI\database\query_builder\mongo_query_builder.py`
and use the commented code (the results will not be sorted by text matching).

If you have problems installing MongoDB see the 
[documentation](https://docs.mongodb.com/manual/tutorial/install-mongodb-enterprise-on-windows).

If the app loads for ever check if you have started MongoDB.

