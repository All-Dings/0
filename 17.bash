#!/bin/bash
#
# Gerate function
#

Script_Directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$Script_Directory/16.bash"

Dings_Dir_Container=/111
Use_Real_Big_Data=false

function Get_Config()
{
	local Name=$1
	jq -r $Name $Dings_Dir/.Dings/Config/Dings-Config
}

function Ls_Names_Md()
{
	local name file

	mwLsNames | while read name;
	do
		file=$(mwName2File "$name")

		printf -- "- [%s](%s)\n" "$name" "$file"
	done
}

function Rsync_Aws_Server()
{
	local Pem_File=$1
	rsync -e "ssh -i $Pem_File" $2 $3 $4 $5 $6 $7 $8 $9
}

function Generate_Md()
{
	printf "# List of all Things\n"
	printf "\n"
	Ls_Names_Md
	printf "\n"
	printf "Generated: $(date)"
}

function Update_Sub_Modules()
{
	local Tag=$1

	cd .Dings/Repositories
	local Repository_List=$(ls)
	for Repository in $Repository_List
	do
		>&2 echo "Updating: $Repository"
		cd $Repository
		git pull origin Master
		git checkout Master
		git pull --rebase
		git tag -d $Tag
		git push --delete origin $Tag
		# git push origin :refs/tags/$Tag
		git tag $Tag
		git push --tags;
		cd ..
	done
	cd ..
	git tag -d $Tag
	git push --delete origin $Tag
	# git push origin :refs/tags/$Tag
	git tag $Tag
	git push --tags;
}

function Generate_Dings()
{
	echo "Generating All_Dings ..."
	Generate_Md > "$Script_Directory/17.md"
}

function Generate_Dings_Fast_And_Correct()
{
	local Dings_File="$Script_Directory/17.md"
	local Name_File="$Script_Directory/0.txt"
	local Temp_File
	local Link
	local First=true

	rm -f $Dings_File

	cat $Name_File | while read -r Line
	do
		if [ "$Line" == "" ]; then
			continue
		elif [ "${Line:0:1}" == " " ]; then
			continue
		elif [ "${Line:0:1}" == "#" ]; then
			if $First; then
				First=false
			else
				echo >> $Dings_File
			fi
			echo $Line  >> $Dings_File
			echo >> $Dings_File
		else
			Dings_Number=$(echo $Line | cut -d " " -f 1)
			Dings_Name_Anonymous=$(echo $Line | cut -d " " -f 2)
			# Link=$(echo $Line | sed -E 's#([0-9]+)\.(md|jpg|ico|mp3|py|bash|html|make|pl|css)[ ]+(.*)#[\3](\1.\2)#g')
			echo "- [$Dings_Name_Anonymous]($Dings_Number)" >> $Dings_File
		fi
	done

	Temp_File=$(mktemp "${Dings_File}.XXXXXX")
	awk '
		/^$/ {
			if (!Last_Was_Blank) {
				print
			}
			Last_Was_Blank = 1
			next
		}
		{
			print
			Last_Was_Blank = 0
		}
	' "$Dings_File" > "$Temp_File"
	mv "$Temp_File" "$Dings_File"
}

function Gen_Big_Data_Stubs
{
	Big_Data_List=$(cd $Dings_Dir/.Dings/Repositories; find . -type l -ls | grep -E "Big-Data/[0-9]+.*" | awk '{print $13}')
	for File_Path in $Big_Data_List; do
		File_Name=$(basename $File_Path)
		if [ ! -f $Dings_Dir/.Dings/Big-Data-Stubs/$File_Name ]; then
			echo "Create: $File_Name"
			touch $Dings_Dir/.Dings/Big-Data-Stubs/$File_Name
		fi
		if [ ! -f $Dings_Dir/.Dings/Big-Data-Stubs/$File_Name.thumb-800.jpg ]; then
			echo "Create: $File_Name (Thumb-800)"
			touch $Dings_Dir/.Dings/Big-Data-Stubs/$File_Name.thumb-800.jpg
		fi
	done
	echo "This Directory contains only Stubs for Big-Data" > $Dings_Dir/.Dings/Big-Data-Stubs/Big-Data-Stubs
}

function Update_Tags
{
	local Tag=$Dings_Day

	if [ "$Tag" == "" ]; then
		>&2 echo "Error: Bash Variable "Dings_Day" not set"
		exit 1
	fi
	Update_Sub_Modules $Tag
}

function Create_Link
{
	local Number_File_Target_Path=$1
	local Number_File_Name=$(basename $Number_File_Target_Path)
	local Number_File_Path=$(find .Dings/Repositories -name $Number_File_Name)
	ln -f -P $Number_File_Path $Number_File_Target_Path
}

function Print_Usage
{
	echo "Usage: 17.bash [-b][-t][-n][-l LINK][-s PEM-FILE]"
	echo ""
	echo "Basic Tool for Dings-System"
	echo ""
	echo "  -l: LINK: Create Hard-Link"
	echo ""
	echo "  -s: Ssh to AWS"
	echo ""
	echo "  -n: Generate Naming-File"
	echo "  -t: Update Tags"
}

while getopts "hbcpl:s:tn" Arg; do
	case $Arg in
	h)
		Print_Usage
		exit 0
		;;
	b)
		Gen_Big_Data_Stubs
		exit 0;
		;;
	s)
		shift $(expr $OPTIND - 1 )
		Rsync_Aws_Server $OPTARG $@
		exit 0;
		;;
	l)
		Create_Link $OPTARG
		exit 0;
		;;
	t)
		Update_Tags
		exit 0
		;;
	n)
		Generate_Dings_Fast_And_Correct
		exit 0
		;;
  esac
done
Print_Usage
