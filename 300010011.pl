# Dings-Lib-Perl

=for comment
The Dings-Lib-Perl is a [Dings-Lib](300010000.md) in [Perl](9010001.md).
=cut

## Imports

use 5.010;
use strict;
use warnings;
use Cwd;

## Directory containing the Markdown files
my $Dings_Directory = getcwd;

## Regular-Expressions

### Get Number from Number-File
my $Number_Regex = qr/^(\d+).md$/;

### Get Heading String from first Line
my $Heading_Regex = qr/^#\s+(.*)\n$/;

## Number-File-List
my %Number_File_List = ();

## Read all Number-Files into a [Linked-List](250000019.md)
sub Read_Number_File_List()
{
	my ($File, $First_Line, $Name, $Number, $Number_File);
	my @File_List;

	### Loop over all Files in the Directory
	opendir(DH, $Dings_Directory);
	@File_List = readdir(DH);
	closedir(DH);

	foreach my $File_Name (@File_List) {
		if ($File_Name !~ /^.*\.md$/) {
			next;
		}
		open my $File, '<', $File_Name;
		my $First_Line = <$File>;
		close $File;

		$First_Line =~ /$Heading_Regex/;
		$Name = $1;

		$File_Name =~ /$Number_Regex/;
		$Number = $1;

		### Define new [Dictionary](250000018.md) for Number-File
		$Number_File = {};
		$Number_File->{'Number'} = $Number;
		$Number_File->{'Name'} = $Name;
		### Append Number-File-Dictionary to Number-File-List
		$Number_File_List{$Number} = $Number_File;
	}
}

## Print all Number-Files
sub Print_Number_File_List()
{
	my $Number_File;

	foreach my $Number_File (values %Number_File_List) {
		printf("%d: %s\n", $Number_File->{'Number'}, $Number_File->{'Name'});
	}
}

## Test Number File
sub Number_File_List_Test()
{
	Read_Number_File_List();
	Print_Number_File_List();
}

Number_File_List_Test();
