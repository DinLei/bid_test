#!/bin/sh 

a=`find ./ -name '*.conf'`
 
if [ "$a" = "" ]; then 
echo "a is not set!" 
else 
echo "a is set !" 
fi

b=
if [ "$b" = "" ]; then
echo "b is not set!" 
else
echo "b is set !" 
fi 
