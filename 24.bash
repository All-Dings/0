#!/bin/bash
#
# # Run Tests
#

# ## Read Tests
#
source 16.bash

# ## Execute Tests
#
function runTests()
{
	local testCases=$(grep 'Test()' 16.bash | cut -b 10-)
	local test

	for test in $testCases; do
		if [[ $test =~ ^([[:alnum:]]+) ]]; then
			local testFunction=${BASH_REMATCH[1]}
			printf "$testFunction: "
			time $testFunction
			printf "\n"
		fi
	done
}

runTests
