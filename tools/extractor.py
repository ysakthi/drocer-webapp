#
# tools/extractor.py
#
# Extract and structure text from Cleveland City Record PDFs.
#

TOOL_NAME = 'Drocer Extractor'
INPUT_PATH = '../data/pdf'
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


def process_pdf(title, path):
    """
    @param title string Title to apply to the document.
    @param path string Path to the input PDF.
    @returns DrocerDocument
    """
    output_document = DrocerDocument(title, path)
    with open(path, 'rb') as pdf_file:
        # setup pdf reader
        pdf_parser = PDFParser(pdf_file)
        pdf_password = ''
        pdf_document = PDFDocument(pdf_parser, pdf_password)
        pdf_rsrcmgr = PDFResourceManager()
        pdf_laparams = LAParams()
        pdf_device = PDFPageAggregator(pdf_rsrcmgr, laparams=pdf_laparams)
        pdf_interpreter = PDFPageInterpreter(pdf_rsrcmgr, pdf_device)
        # process document
        page_number = 0
        for pdf_page in PDFPage.create_pages(pdf_document):
            page_number += 1
            logger.info("processing %s page number %s" % (title, page_number))
            output_page = DrocerPage(page_number)
            pdf_interpreter.process_page(pdf_page)
            pdf_layout = pdf_device.get_result()
            box_number = 0
            for pdf_obj in pdf_layout:
                if isinstance(pdf_obj, LTTextBox):
                    box_number += 1
                    output_box = DrocerBox(
                        page_number,
                        box_number,
                        pdf_obj.x0,
                        pdf_obj.y0,
                        pdf_obj.x1,
                        pdf_obj.y1,
                        pdf_obj.get_text().encode('utf8')
                    )
                    output_page.boxes.append(output_box)
                else:
                    #logger.debug("non-text object")
                    pass
            output_document.pages.append(output_page)
    return output_document

def write_json(output_directory, document):
    """
    @param output_directory string Directory to write output files.
    @param document DrocerDocument
    Output filename is determined from document source filename.
    """
    output_filename = '%s.json' % (os.path.split(document.source_document_path)[1].split('.')[0])
    output_path = os.path.join(output_directory, output_filename)
    with open(output_path, 'w') as f:
        #json.dump(document, f, default=DrocerSerializable.serialize) #old
        f.write(jsonpickle.encode(document))


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
    pattern = re.compile('([A-Z][a-z]*)([0-9][0-9]?)([0-9]{4})\.pdf')
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
            document = process_pdf(document_title, document_path)
            document_metadata.add_page_location_to_boxes(document)
            document_metadata.add_parcel_numbers_to_document(document)
            document_metadata.add_ordres_numbers_to_document(document)
            document_metadata.add_calendar_numbers_to_document(document)
            write_json(OUTPUT_PATH, document)
        else:
            logger.info('Skipping input file: %s' % filename)

    elapsed = timeit.default_timer() - start_time
    logger.info('%s complete.  Run time %ss' % (TOOL_NAME, elapsed))


