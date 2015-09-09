#!/bin/bash
#q7.sh
echo "Please enter the artist_name: (all in lowercase)"
read artist_name
echo "Please enter the start_year: (inclusive)"
read start_year
echo "Please enter the end_year: (inclusive)"
read end_year
echo "$artist_name,$start_year, $end_year"
count=0
shopt -s nocasematch
cat million_songs_metadata.csv | while read LINE
do
IFS="," read -ra STR_ARRAY <<< "$LINE"
name=${STR_ARRAY[6]}
year=${STR_ARRAY[10]}
if [[ "$artist_name" = "$name" ]] && [[ $year -ge $start_year ]] && [[ $year -le $end_year ]];then
echo "$name"
echo "$year"
count=$(( $count + 1 ))
echo "$count"
fi
done
shopt -u nocasematch