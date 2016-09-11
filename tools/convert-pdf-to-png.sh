#!/bin/bash
#
# Script to convert PDF files in input directory into single-page PNGs
# in the output directory.
#
# Depends on "convert" script from the ImageMagick suite.
# See http://www.imagemagick.org/script/convert.php
#
# Choose your own adventure: getting page count from PDFs in bash
#  1. foo=$(strings < pdffile.pdf | sed -n 's|.*/Count -\{0,1\}\([0-9]\{1,\}\).*|\1|p' | sort -rn | head -n 1)
#  2. foo=$(pdfinfo pdffile.pdf | grep Pages | awk '{print $2}')
#  3. foo=$(pdftk pdffile.pdf dump_data|grep NumberOfPages| awk '{print $2}')
#
#  
#

FILES=../data/pdf/*.pdf
OUTPUT_PATH=../data/png

echo "Drocer: convert PDF to PNG"
for f in $FILES; do
    page_count=$(strings < $f | sed -n 's|.*/Count -\{0,1\}\([0-9]\{1,\}\).*|\1|p' | sort -rn | head -n 1)
    page_counter=0
    counting_counter=1
    while [ $page_counter -lt $page_count ]; do
        echo "Processing input file $f page $counting_counter"
        output_basename=`echo $f|sed -e's/.*\/\(.*\)\.pdf/\1/'`
        output_filename="$OUTPUT_PATH/$output_basename-$counting_counter.png"
        echo "Writing output to $output_filename"
        convert -density 300 $f[$page_counter] -resize 2550x3300 $output_filename
        let page_counter=page_counter+1
        let counting_counter=counting_counter+1
    done
done
