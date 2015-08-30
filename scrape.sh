#!/bin/bash
date=$(date +%s | tr -d ' ')

dir=data-$date
mkdir $dir
wget -i filelist -P $dir &> $dir/wget.log 
grep "Shares Traded" $dir/* -l >$dir/valid
grep "Shares Traded" $dir/* -L >$dir/invalid
`dirname $0`/parse.py $date
