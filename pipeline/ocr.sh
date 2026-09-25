#!/bin/sh
cd "$(dirname "$0")"
export OMP_THREAD_LIMIT=1
ls png/*.png | xargs -P 4 -I{} sh -c 'o=ocr/$(basename {} .png).txt; [ -s $o ] || { tesseract {} - -l jpn --psm 6 > $o.tmp 2>/dev/null && mv $o.tmp $o; }'
ls ocr/*.txt | wc -l
