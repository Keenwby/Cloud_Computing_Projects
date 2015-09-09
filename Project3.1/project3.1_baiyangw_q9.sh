#!/bin/bash
#q9.sh
export LC_CTYPE=C
export LANG=C
join -t ',' -a1 -a2 -1 1 -2 1 ./million_songs_sales_data.csv ./million_songs_metadata.csv >million_songs_metadata_and_sales.csv
awk 'BEGIN {FS = ","}{a[$7]+=$3} END{for(i in a)print i,a[i]}' million_songs_metadata_and_sales.csv | sort -k2nr | awk 'NR==1 {print$0}'
