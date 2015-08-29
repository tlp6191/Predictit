#!/bin/bash
dir=data-$(date | tr -d ' ')
mkdir $dir
wget -i filelist -P $dir &> $dir/wget.log 
grep "Shares Traded" $dir/* -l >$dir/valid
grep "Shares Traded" $dir/* -L >$dir/invalid
