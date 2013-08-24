#!/bin/sh

for dir in ${PATH//:/ }; do
  CMDS="$CMDS `ls $dir/nosetests-* 2>/dev/null`"
done

CMDS=`echo $CMDS | sed -e 's/^ *//g' -e 's/ *$//g'`

if [ -z "$CMDS" ]; then
    if [ `command -v nosetests` ]; then
        testcmd=nosetests
    else
        echo "No versions of Nose found"
    fi
else
    CMDS=(`echo $CMDS |xargs -n1|sort -r`)
    testcmd=${CMDS[0]}
fi

echo "Using nose version: $testcmd"
$testcmd -v $1