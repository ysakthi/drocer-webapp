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
#  Notes:
#   - With 500kB per page, total image storage will be about 20GB
#   - Show dimensions at 90 dpi: convert -density 90 ../pdf/August312016.pdf[0] info:
#   - View with: eog filename.png
#   - Total file size in directory: ls -l | gawk '{sum += $5} END {print sum;}'
#   - Average file size in directory: ls -l | gawk '{sum += $5; n++;} END {print sum/n;}'
#   - 90 dpi is too low even at high quality-- text is very pixelated
#   - 200 dpi, 75 quality = ~1MB per page
#   - 175 dpi, 10 quality = ~500kB per page
#

FILES=../data/pdf/*.pdf
OUTPUT_PATH=../data/png
DPI=175
QUALITY=10

echo "Drocer: convert PDF to PNG"
for f in $FILES; do
    page_count=$(strings < $f | sed -n 's|.*/Count -\{0,1\}\([0-9]\{1,\}\).*|\1|p' | sort -rn | head -n 1)
    page_counter=0
    counting_counter=1
    while [ $page_counter -lt $page_count ]; do
        echo "Processing input file $f page $counting_counter"
        output_size==`convert -density $DPI $f[$page_counter] info:|awk '{print $3}'`
        output_basename=`echo $f|sed -e's/.*\/\(.*\)\.pdf/\1/'`
        output_filename="$OUTPUT_PATH/$output_basename-$counting_counter.png"
        echo "Writing output to $output_filename"
        convert -density $DPI $f[$page_counter] -quality $QUALITY $output_filename
        let page_counter=page_counter+1
        let counting_counter=counting_counter+1
    done
done
