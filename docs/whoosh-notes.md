# Configuring Whoosh for Drocer

## Whoosh configuration

see: https://whoosh.readthedocs.io/en/latest/quickstart.html

### define schema
```
from whoosh.fields import Schema, TEXT
schema = Schema(title=TEXT, content=TEXT)

from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
schema = Schema(title=TEXT(stored=True), content=TEXT, path=ID(stored=True), tags=KEYWORD, icon=STORED)
```
### define index
A whoosh index lives in a directory.
```
import os.path
from whoosh.index import create_in

INDEX_PATH = '../data/example-index'

if not os.path.exists(INDEX_PATH):
    os.mkdir(INDEX_PATH)

ix = create_in(INDEX_PATH, schema)

from whoosh.index import open_dir
ix = open_dir(INDEX_PATH)
```
### write to the index
```
writer = ix.writer()
writer.add_document(title=u"My document", content=u"This is my document!",
                    path=u"/a", tags=u"first short", icon=u"/icons/star.png")
writer.add_document(title=u"Second try", content=u"This is the second example.",
                    path=u"/b", tags=u"second short", icon=u"/icons/sheep.png")
writer.add_document(title=u"Third time's the charm", content=u"Examples are many.",
                    path=u"/c", tags=u"short", icon=u"/icons/book.png")
writer.commit()
```
### search the index
 - queries may be constructed directly, as in first example
 - queries may be parsed according to schema field, as in second example
 - queries may be parsed according to multiple fields
```
searcher = ix.searcher()

from whoosh.query import *
myquery = And([Term("content", u"apple"), Term("content", "bear")])

from whoosh.qparser import QueryParser
parser = QueryParser("content", ix.schema)
myquery = parser.parse(querystring)

mparser = MultifieldParser(["title", "content"], schema=myschema)

```

Putting it all together:
```
querystring = "examples"
from whoosh.qparser import QueryParser
res = None
with ix.searcher() as searcher:
    parser = QueryParser("content", ix.schema)
    myquery = parser.parse(querystring) 
    results = searcher.search(myquery)
    for result in results:
        print result


```
