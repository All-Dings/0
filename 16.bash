#!/bin/bash
#
# # Bash Library for this project
#

Null=""

function mwReturnOnNull()
{
	local returnString=$1

	if [[ "$returnString" == "$Null" ]]; then
		return 1
	fi
}

function mwReturnString()
{
	local returnString=$1

	if [[ "$returnString" == "$Null" ]]; then
		return 1
	else
		echo $returnString
	fi
}

function mwReturnOnNullTest()
{
	local undefined

	$(mwReturnOnNull $Null)
	echo $?
	$(mwReturnOnNull $undefined)
	echo $?
}


function mwReturn()
{
	local returnValue=$1

	echo $returnValue
	return 1
}

function mwReturnPanic()
{
	local message="$1" frame=0 frameWithHash line function file

	>&2 printf "\n"
	>&2 printf "LibBash: $message\n"
	>&2 printf "\n"
	# >&2 printf "         %5s %20s %-20s %s\n" "FRAME" "FILE" "FUNCTION" "LINE"
	while read line function file < <(caller "$frame");
	do
		file=$(basename "$file")
		mwReturnOnNull $file
		function="$function()"
		frameWithHash="#$frame"

		if [[ $frame == 0 ]]; then
			>&2 printf "      %5s %20s %-20s %s <== Bug was detected here\n" $frameWithHash $file $function $line
		else
			>&2 printf "      %5s %20s %-20s %s\n" $frameWithHash $file $function $line
		fi
		((frame++))
	done
	>&2 printf "\n"
	mwReturn $Null
}

function mwName2File()
{
	local name=$1

	for file in $(ls *.md);
	do
		local header=$(mwFile2Header "$file")
		mwReturnOnNull $header
		local nameFile=$(mwHeader2Name "$header")
		mwReturnOnNull $nameFile
		if [[ "$name" == $nameFile ]]; then
			echo $file
			return
		fi
	done

	mwReturnPanic "No corresponding File for Name \"$name\" found"
}

function mwName2FileTest()
{
	local file=$(mwName2File "Michael Holzheu")
	mwReturnString $file
}

function mwName2Number()
{
	local name=$1
	local file=$(mwName2File "$name")
	mwReturnOnNull $file

	if [[ $file =~ ([[:digit:]]+).md ]]; then
		local number=${BASH_REMATCH[1]}
		2&> echo "$number"
		echo $number
		return
	fi
	mwReturnPanic "No corresponding File for Name \"$name\" found"
}

function mwName2NumberTest()
{
	# local number=$(mwName2Number "Michael Holzheu")
	local number=$(mwName2Number "All Things")
	mwReturnOnNull $number

	echo "$number"
}

function mwFile2Header()
{
	local numberFile=$1

	head -1 $numberFile
}

function mwFile2HeaderTest()
{
	local header=$(mwFile2Header "0.md")
	mwReturnString $header
}

function mwHeader2Name()
{
	local header=$1

	echo $header | cut -b 3-
}

function mwHeader2NameTest()
{
	local name=$(mwHeader2Name "# Michael Holzheu")
	mwReturnString $name
}

function mwNumber2Name()
{
	local number=$1
	local header
	local name

	header=$(mwNumber2Header "$number")
	mwReturnOnNull $header
	name=$(mwHeader2Name "$header")
	mwReturnString $name
}

function mwNumber2NameTest()
{
	local name=$(mwNumber2Name "0")
	mwReturnString $name
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
	mwReturnString $header
}

function mwLsNumbersUnsorted()
{
	for md in $(ls *.md);
	do
		local number=$(basename "$md" ".md")
		if [[ $number =~ ^[[:digit:]]+$ ]];
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
