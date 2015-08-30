#!/bin/bash
date=$(date +%s | tr -d ' ')

dir=data-$date
localdir=`dirname $0`
mkdir $localdir/$dir
wget -i $localdir/filelist -P $localdir/$dir &> $localdir/$dir/wget.log 
grep "Shares Traded" $localdir/$dir/* -l |xargs grep "Buy Yes" -l >$localdir/$dir/last_valid
grep "Shares Traded" $localdir/$dir/* -l |xargs grep "Buy Yes" -l >$localdir/$dir/active
grep "Shares Traded" $localdir/$dir/* -L >$localdir/$dir/invalid
$localdir/parse.py $date $localdir
#rm $localdir/$dir/SingleOption*
$localdir/recal_filelist.py $date $localdir/data-$date >$localdir/filelist
