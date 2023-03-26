#!/bin/bash
#
# Gerate function
#

source 16.bash


function lsNamesMd()
{
	local name file

	mwLsNames | while read name;
	do
		file=$(mwName2File "$name")
		
		printf "- [%s](%s)\n" "$name" "$file"
	done
}

function generateMd()
{
	printf "# List of all Things\n"
	printf "\n"
	lsNamesMd
	printf "\n"
	printf "Generated: $(date)"
}

function generate()
{
	generateMd > 17.markdown	
}
