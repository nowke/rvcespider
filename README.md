# RVCE Spider
Crawler for RVCE Results Site

## Clone the Repository
```shell
$ git clone https://github.com/nowke/rvcespider.git
```

## Create a virtualenv
```shell
$ mkvirtualenv rvcespider
```

## Install dependencies
```shell
$ pip install -r requirements.txt
```

## Create directories for storing results
```shell
$ mkdir jsons
$ mkdir ojson
```

## Set the semesters to crawl in start_crawl.py
```
Semester = [1,5]
```

## Start crawl
```shell
python start_crawl.py
```

JSON Files available in ```ojson``` folder