#!/bin/bash
#
# # Bash tests
#

# ## Pass Arguments with blanks
#
function functionBlankArguments1()
{
	local arg1=$1
	local arg2=$2
	local arg3=$3

	printf "Arg1: \"$arg1\"\n"
	printf "Arg2: \"$arg2\"\n"
	printf "Arg3: \"$arg3\"\n"
}

function functionwithBlankArguments2()
{
	local arg1="$1"
	local arg2="$2"
	local arg3="$3"

	printf "Arg1: \"$arg1\"\n"
	printf "Arg2: \"$arg2\"\n"
	printf "Arg3: \"$arg3\"\n"
}

function functionWithBlankArgumentsTest()
{
	functionWithBlankArguments1 One Two Three
	functionWithBlankArguments2 One Two Three

	functionWithBlankArguments1 "One Two Three"
	functionWithBlankArguments2 "One Two Three"
}

# ## Test
#
function testTest()
{
	local test="yes"

	[[ $test == "yes" ]]
	echo $?

	test $test == "yes"
	echo $?

	test $test = "yes"
	echo $?

	[[ $tes == "no" ]]
	echo $?

	test $test == "no"
	echo $?

	test $test = "no"
	echo $?

}

# # Regular expressions

# ## Match without if
#
function regexDigitTest()
{
	local input

	input="0.md"
	[[ $input =~ ([[:digit:]]+).md ]]
	echo "rc=$?"
	echo "match0: ${BASH_REMATCH[0]}"
	echo "match1: ${BASH_REMATCH[1]}"
	echo "match2: ${BASH_REMATCH[2]}"
}

# ## Match with if
#
function regexFileTest()
{
	local input

	input="17.md"
	if [[ $input =~ ([[:digit:]]+).md ]]; then
		local number=${BASH_REMATCH[1]}
		2&> echo "$number"
		echo $number
	fi
}

# ## Undefined variables
#
function undefinedVariablesTest()
{
	local undefined

	echo "\"$undefined\""

	test "$undefined" == ""
	echo $?
}

# ## Minus and printf
#
# - Minus sign at start of string: http://www.das-werkstatt.com/forum/werkstatt/viewtopic.php?t=1959
#
function minusPrintfTest()
{
	# printf "- test"
	printf -- "- test"
}

# ## Single and double brackets
#
# - Compare "[" and "[[": https://stackoverflow.com/questions/3427872/whats-the-difference-between-and-in-bash
#
function bracketTest()
{
	local test="test eins"

	[ $test == "test eins" ]
	echo $?

	[ "$test" == "test eins" ]
	echo $?

	[[ $test == "test eins" ]]
	echo $?
}
