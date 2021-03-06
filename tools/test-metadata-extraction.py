#
# tools/test-metadata-extraction.py
#
# Test metadata extraction methods on extracted JSON documents.
#

TOOL_NAME = 'Drocer Metadata Extraction Test'
INPUT_PATH = '../data/json'
OUTPUT_PATH = '../data/json'

import logging
import json
import jsonpickle
import os
import re
import timeit

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox

from modules.document_structure import DrocerSerializable
from modules.document_structure import DrocerDocument
from modules.document_structure import DrocerPage
from modules.document_structure import DrocerBox

from modules import document_metadata


if __name__ == '__main__':
    # Setup logging.
    import logging
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(module)s.%(funcName)s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting %s.' % TOOL_NAME)
    logger.info('Reading PDF files from %s.' % INPUT_PATH)
    logger.info('Writing JSON files to %s.' % OUTPUT_PATH)

    # Setup timer.
    start_time = timeit.default_timer()

    # Process files.
    pattern = re.compile('([A-Z][a-z]*)([0-9][0-9]?)([0-9]{4})\.json')
    for filename in os.listdir(INPUT_PATH):
        result = pattern.match(filename)
        if result:
            logger.info('Processing input file: %s' % filename)
            document_title = "Cleveland City Record %s %s, %s" % (
                result.group(1),
                result.group(2),
                result.group(3)
            )
            document_path = os.path.join(INPUT_PATH, filename)
            with open(document_path, 'r') as input_file:
                document = jsonpickle.decode(input_file.read())
                document_metadata.add_page_location_to_boxes(document)
                document_metadata.add_parcel_numbers_to_document(document)
                document_metadata.add_ordres_numbers_to_document(document)
                document_metadata.add_calendar_numbers_to_document(document)
                #write_json(OUTPUT_PATH, document)
        else:
            logger.info('Skipping input file: %s' % filename)

    elapsed = timeit.default_timer() - start_time
    logger.info('%s complete.  Run time %ss' % (TOOL_NAME, elapsed))
