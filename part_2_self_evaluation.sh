#!/bin/sh

if [ ! -e "./README" ]
then
	echo "Error: No README file"
	exit 1
fi

if [ ! -e "./Makefile" ]
then
	echo "Error: No Makefile file"
	exit 1
fi

echo "Running make"
make
rc=$?
if [ $rc -ne 0 ]
then
	echo "Error when running the make command"
	exit 1
fi

if [ ! -e "./client" ]
then
	echo "Error: Running make did not create the client file"
	exit 1
fi

if [ ! -x "./client" ]
then
	echo "Error: client file is not executable"
	exit 1
fi

echo "Running ./client GET http://www.msftncsi.com/ncsi.txt"
simple_output=$(./client GET http://www.msftncsi.com/ncsi.txt)
rc=$?
if [ $rc -ne 0 ]
then
	echo "Error: fetching the test page http://www.msftncsi.com/ncsi.txt"
	exit 1
fi

if [ "$simple_output" != "Microsoft NCSI" ]
then
	echo "Error: output from simple command was not correct"
	exit 1
fi

echo "Checking that ./client GET http://www.msftncsi.com/ncsi.txt outputs the right number of characters"
chars=$(./client GET http://www.msftncsi.com/ncsi.txt | wc -c)
if [ "$chars" -ne 14 ]
then
	echo "Error: wrong number of characters returned for http://www.msftncsi.com/ncsi.txt"
	echo "Should be exactly 14 characters yet you returned $chars"
	exit 1
fi

echo "Running ./client PUT http://sefcom.asu.edu/"
test_error=$(./client PUT http://sefcom.asu.edu/)
rc=$?
if [ $rc -ne 4 ]
then
	echo "Error: the status code not set properly"
	exit 1
fi

echo "Running ./client GET http://sefcom.asu.edu"
bigger_test=$(./client GET http://sefcom.asu.edu)
rc=$?
if [ $rc -ne 0 ]
then
	echo "Error: Third test case did not execute correctly"
	exit 1
fi

echo "Great Success! Assuming that your code compiles on an Ubuntu 14.04 you should get at least 70%"
