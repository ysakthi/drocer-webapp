#
# document_metadata.py
#
# Functions for adding metadata to documents.
#

import re
from document_structure import DrocerMetadata

def add_page_location_to_boxes(document):
    """
    @param document DrocerDocument
    """
    for page in document.pages:
        for box in page.boxes:
            if box.y0 < 72 :
                box.add_metadata('page_location', 'footer')
            elif box.y1 > 724:
                box.add_metadata('page_location', 'header')
            else:
                box.add_metadata('page_location', 'body')

# match parcel numbers
def add_parcel_numbers_to_document(document):
    """
    @param document DrocerDocument
    """
    for page in document.pages:
        for box in page.boxes:
            matcher = re.compile('([0-9]{3})-?([0-9]{2})-?([0-9]{3}[a-zA-Z]?)')
            result = matcher.search(box.text)
            if result:
                parcel_number = result.group(0)
                metadata = DrocerMetadata({
                    'parcel_number': parcel_number,
                    'page_number': box.page_number,
                    'box_number': box.number
                })
                document.add_metadata('parcel_numbers', metadata)
                #print "page: %s, box %s: %s in %s" % (page.number, box.number, result.group(0), box.text)

# match ord-res numbers
def add_ordres_numbers_to_document(document):
    """
    @param document DrocerDocument
    """
    for page in document.pages:
        for box in page.boxes:
            matcher = re.compile('[0-9]{3}-[0-9]{2}')
            result = matcher.search(box.text)
            if result:
                ordres_number = result.group(0)
                metadata = DrocerMetadata({
                    'ordres_number': ordres_number,
                    'page_number': box.page_number,
                    'box_number': box.number
                })
                document.add_metadata('ordres_numbers', metadata)
                #print "page: %s, box %s: %s in %s" % (page.number, box.number, result.group(0), box.text)
