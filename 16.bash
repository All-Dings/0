#!/bin/bash
#
# Bash Library for this project
#

function mwExit()
{
	local message=$1 frame=0 line sub file

	>&2 printf "LibBash: $message\n"
	while read line sub file < <(caller "$frame");
	do
		if [[ $frame == 0 ]]; then
			>&2 printf "         #%s %s() at %s:%s <== Bug was detected here\n" $frame $sub $file $line
		else
			>&2 printf "         #%s %s() at %s:%s\n" $frame $sub $file $line
		fi
		((frame++))
	done
	exit 1
}

function mwName2File()
{
	local name=$1

	for file in $(ls *.md);
	do
		local header=$(mwFile2Header "$file")
		local nameFile=$(mwHeader2Name "$header")
		if [[ "$name" == "$nameFile" ]]; then
			echo $file
			return
		fi
	done

	mwExit "No corresponding File for Name \"$name\" found"
}

function mwName2FileTest()
{
	local file=$(mwName2File "Michael Holzheu")

	echo $file
}

function mwFile2Header()
{
	local numberFile=$1

	head -1 $numberFile
}

function mwFile2HeaderTest()
{
	local header=$(mwFile2Header "0.md")

	echo $header
}

function mwHeader2Name()
{
	local header=$1

	echo $header | cut -b 3-
}

function mwHeader2NameTest()
{
	local name=$(mwHeader2Name "# Michael Holzheu")

	echo $name
}

function mwNumber2Name()
{
	local number=$1
	local header
	local name

	header=$(mwNumber2Header "$number")
	name=$(mwHeader2Name "$header")

	echo $name
}

function mwNumber2NameTest()
{
	local name=$(mwNumber2Name "0")

	echo $name	
}

function mwNumber2Header()
{
	local number=$1
	local file="$number.md"

	mwFile2Header $file
}

function mwNumber2HeaderTest()
{
	local header=$(mwNumber2Header "0");

	echo $header
}

function mwLsNumbersUnsorted()
{
	for md in $(ls *.md);
	do
		local number=$(basename "$md" ".md")
		if [[ $number =~ '^[0-9]+$' ]];
		then
			echo "$number"
		fi
	done
}

function mwLsNumbers()
{
	mwLsNumbersUnsorted | sort -n
}

function mwLsNamesUnsorted()
{
	for file in $(ls *.md);
	do
		local name=$(head -1 $file | cut -b 3-)
		echo $name
	done
}

function mwLsNames()
{
	mwLsNamesUnsorted | sort
}

function mwPrintForEachLine()
{
	local fn1="$1"
	local fn2="$2"

	$fn1 | while read line ; do $fn2 "$line"; done
}
