# Introduction
Search engines now really bloated with AI and other stuff, so I wanted to write my own one
This is Simple Web Crawler which uses selenium to parse more data from the site

# Instalation
It is written in python, so all you'll need to install it is
```sh
pip install -r requirements.txt
````

# Usage
then to start crawling just run
## First Start
```sh
python main.py
```

default starting page for crawling is https://thebestmotherfucking.website/
but if you want to start from a particular website (or websites) you can run
```sh
python main.py [your websites list]
```

## Second start
After every interruptin, crawler will save urls that it was going to crawl but didn't crawl yet in a gonna_crawl.txt file
this file may be used on a next run to start from the last place via
```sh
python main.py $(cat gonna_crawl.txt)
```
Warning: gonna_crawl.txt file will be overwritten on every interruption

# Getting the results
Crawler saves results in database.db file which is SQLite3 database
