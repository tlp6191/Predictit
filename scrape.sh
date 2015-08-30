#!/bin/bash
date=$(date +%s | tr -d ' ')

dir=data-$date
localdir=`dirname $0`
mkdir $localdir/$dir
wget -i $localdir/filelist -P $localdir/$dir &> $localdir/$dir/wget.log 
grep "Shares Traded" $localdir/$dir/* -l >$localdir/$dir/valid
grep "Shares Traded" $localdir/$dir/* -L >$localdir/$dir/invalid
$localdir/parse.py $date
rm $localdir/$dir/SingleOption*
$localdir/recal_filelist.py $date >$localdir/filelist
