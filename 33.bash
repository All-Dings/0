#!/bin/bash
#
# # Bash Commands for his Project
#

# ## Include Bash Library
#
source 16.bash

# ## mmls
#
# List all Things
#
function mmls()
{
        local name number

        mwLsNames | while read name;
        do
                number=$(mwName2Number "$name")
		mwReturnOnNull $number

                printf "%3s: %s\n" "$number" "$name"
        done
}
