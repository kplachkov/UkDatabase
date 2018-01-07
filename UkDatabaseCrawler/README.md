UkDatabaseCrawler
=================

The "UkDatabaseCrawler" is crawler created to scrape [https://theukdatabase.com](https://theukdatabase.com) for 
information about people based on posts.

## Requirements


  * Python 3 or higher;
  * MongoDB;
  * Scrapy;
  * bs4;
  * pymongo;
  
If unsure about meeting these requirements, download the crawler and
browse the [Flask](http://flask.pocoo.org/docs/0.12), 
[MongoDB](https://docs.mongodb.com) and 
[PyMongo](https://api.mongodb.com/python/current)
documentation to get more detailed information.

## Installation


First, install [Python 3](https://www.python.org) and [MongoDB](https://www.mongodb.com)
if you haven't already. Then, install pymongo, bs4 and scrapy by executing
these commands anywhere in your system:


```terminal
$ pip install pymongo
```

```terminal
$ pip install bs4
```

```terminal
$ pip install Scrapy
```

If you have problems installing Scrapy use the following command: 

```terminal
$ conda install -c conda-forge scrapy
```

If the `pip` command is not available, update your package manager to the
most recent version executing the  
`python -m pip install --upgrade pip` command (Windows).

## Usage

First start the `mongod.exe` from `~\MongoDB\Server\3.6\bin` or just type 
`mongod` in the command prompt (if а path to the bin folder is available).
Then open the command prompt (terminal) from `~\UkDatabaseCrawler\UkDatabase\spiders` 
and type one of the following commands:

```terminal
$ scrapy runspider uk_database_site.py
```

or

```terminal
$ scrapy runspider uk_database_posts.py
```
This will start a spider.

The `uk_database_site.py` spider scrapes the whole website, iterating
over all the links part of the domain [https://theukdatabase.com](https://theukdatabase.com).

The `uk_database_posts.py` spider starts scraping post by post.

You can see the scraped information in 
`~\UkDatabase\UkDatabase\crawled_info\TheUkDatabase.json`
or in the MongoDB database.

***In case you are not going to use the spiders with MongoDB,
use the following command:**

```terminal
$ scrapy crawl <spider_name> -s ITEM_PIPELINES="{}"
```

This will generate only a .json file with the scraped information.

## How to deploy the crawler

### Deploying Spiders

This section describes the different options you have 
for deploying your Scrapy spiders to run them on a regular 
basis. Running Scrapy spiders in your local machine is very 
convenient for the (early) development stage, but not so 
much when you need to execute long-running spiders or move 
spiders to run in production continuously. This is where 
the solutions for deploying Scrapy spiders come in.

Popular choices for deploying Scrapy spiders are:

* [Scrapyd](https://doc.scrapy.org/en/latest/topics/deploy.html#deploy-scrapyd) (open source)
* [Scrapy Cloud](https://doc.scrapy.org/en/latest/topics/deploy.html#deploy-scrapy-cloud) (cloud-based)

### Deploying to a Scrapyd Server
Scrapyd is an open source application to run Scrapy 
spiders. It provides a server with HTTP API, capable of 
running and monitoring Scrapy spiders.

To deploy spiders to Scrapyd, you can use the scrapyd-deploy 
tool provided by the scrapyd-client package. Please refer to 
the scrapyd-deploy documentation for more information.

Scrapyd is maintained by some of the Scrapy developers.

### Deploying to Scrapy Cloud
[Scrapy Cloud](https://scrapinghub.com/scrapy-cloud) is a hosted, 
cloud-based service by Scrapinghub, the company behind Scrapy.

Scrapy Cloud removes the need to setup and monitor servers and 
provides a nice UI to manage spiders and review scraped items,
logs and stats.

To deploy spiders to Scrapy Cloud you can use the shub command 
line tool. Please refer to the Scrapy Cloud documentation for 
more information.

Scrapy Cloud is compatible with Scrapyd and one can switch between 
them as needed - the configuration is read from the scrapy.cfg file 
just like scrapyd-deploy.

***Before deploying the crawler change the MongoDB URI and 
the MongoDB database name to your preference.**
(`~\UkDatabaseCrawler\UkDatabaseCrawler\settings.py`)

```python
MONGO_URI = "mongodb://localhost:27017"
```
```python
MONGO_DATABASE = 'UkDatabase'
```

Troubleshooting
---------------

If you get this message:
`No connection could be made because the target machine actively refused it`
check [Usage](##Usage).

If you have problems installing MongoDB see the 
[documentation](https://docs.mongodb.com/manual/tutorial/install-mongodb-enterprise-on-windows).
