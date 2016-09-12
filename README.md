# Drocer Web Application

Flask web application for serving the Drocer web application.

## Installation
```
(clone repo)
cd (local repo directory)
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Extraction and indexing.

 - Download source PDFs from [Cleveland City Council](http://www.clevelandcitycouncil.org/legislation-laws/the-city-record) and place in `data/pdf`.
 - Enter tools directory, run the extractor: `python extractor.py`.  This writes JSON files to `data/json`.
 - Enter tools directory, run the indexer: `python indexer.py`.  This creates a Whoosh index in `data/index/city-record`.
 - Enter tools directory, run the image extractor script: `./convert-pdf-to-png.sh`.  This creates a PNG file for each page in the source PDFs.

## Running the web server

 - Development environment server: `python run.py`.
 - Production server configuration is defined in drocer.wsgi

## Baked-in Dependencies
 - [jQuery](https://jquery.com/)
 - [Materialize CSS](http://materializecss.com/)
 - [Prism JS](http://prismjs.com/)
