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

my $Reg_Exp_Number_File = '\d+' . '.' . '\w+';
my $Reg_Exp_Name_Exact = '(' . '\"|=|\?|\!|\:|\(|\)|#|-|\w|\s|@' . ')' . '+';
my $Reg_Exp_Name = '(' . '.' . ')' . '+';

### Apply [Reg_Exp](9000103.md) to [Line](700011.md) and print the [Match](404.md)
sub Reg_Exp_Test($$)
{
	my $Reg_Exp = $_[0];
	my $Line = $_[1];
	my $Match;

	$Line =~ /$Reg_Exp/;
	$Match = $1;
	printf("\"%s\" -> \"%s\"\n", $Line, $Match);
}

### Get Dings-Name from First-Line
my $Name_Reg_Exp = '^' . '#' . ' ' . '(' . $Reg_Exp_Name . ')' . '\s*' . '$';

sub Name_Reg_Exp_Test()
{
	Reg_Exp_Test($Name_Reg_Exp, '# Michael-Holzheu');
	Reg_Exp_Test($Name_Reg_Exp, '# Michael Holzheu');
	Reg_Exp_Test($Name_Reg_Exp, '# Michael-Holzheu-Neu');
	Reg_Exp_Test($Name_Reg_Exp, '# michael-holzheu@Git-Hub');
	Reg_Exp_Test($Name_Reg_Exp, '# Michael_Holzheu-Neu');
	Reg_Exp_Test($Name_Reg_Exp, '# Brașov');
}

### Get Number from Number-File
my $Number_Reg_Exp = '^' . '(' . '\d+' . ')' . '.md' . '$';

sub Number_Reg_Exp_Test()
{
	Reg_Exp_Test($Number_Reg_Exp, '0.md');
	Reg_Exp_Test($Number_Reg_Exp, '341324.md');
}

### Get Reference from Line
my $Reference_Reg_Exp = '(' . '\[' . $Reg_Exp_Name . '\]' . '\(' . $Reg_Exp_Number_File . '\)' . ')';

sub Reference_Reg_Exp_Test()
{
	Reg_Exp_Test($Reference_Reg_Exp, 'The Man [Michael-Holzheu](0.md) creates the Dings-Project.');
	Reg_Exp_Test($Reference_Reg_Exp, '[Michael-Holzheu](0.md) builds Dings-Project.');
	Reg_Exp_Test($Reference_Reg_Exp, 'The Digns-Prject is created by [Michael-Holzheu](0.md)');
}

### Get Name from Reference
my $Name_from_Reference_Reg_Exp = '\[' . '(' . $Reg_Exp_Name . ')' . '\]' . '\(' . $Reg_Exp_Number_File . '\)';

sub Name_from_Reference_Reg_Exp_Test()
{
        Reg_Exp_Test($Name_from_Reference_Reg_Exp, '[Michael-Holzheu](0.md)')
}

## Number-File-List
my %Number_File_List = ();

## Print Number-File
sub Print_Number_File($)
{
	my $Number_File = $_[0];
	my $Name = $Number_File->{'Name'};
	my $Number = $Number_File->{'Number'};
	printf("%d \"%s\"\n", $Number, $Name);
}

## Remove White-Space from the Start and End of a String
sub Strip($)
{
	my $String = $_[0];
	$String =~ s/^\s+|\s+$//g;
	return $String;
}

## Read Data of a Number-File
sub Read_Number_File($)
{
	my ($Name, $Number, $Number_File);
	my $File_Name = $_[0];

	open my $File, '<', $File_Name;
	my $First_Line = <$File>;
	close $File;

	$First_Line = Strip($First_Line);
	$First_Line =~ /$Name_Reg_Exp/;
	$Name = $1;

	$File_Name =~ /$Number_Reg_Exp/;
	$Number = $1;

	### Define new [Dictionary](250000018.md) for Number-File
	$Number_File = {};
	$Number_File->{'Number'} = $Number;
	$Number_File->{'Name'} = $Name;

	return $Number_File;
}

## Read all Number-Files into a [Linked-List](250000019.md)
sub Read_Number_File_List()
{
	my $Number_File;
	my @File_List;

	### Loop over all Files in the Directory
	opendir(DH, $Dings_Directory);
	@File_List = readdir(DH);
	closedir(DH);

	foreach my $File_Name (@File_List) {
		if ($File_Name !~ /$Number_Reg_Exp/) {
			next;
		}
		$Number_File = Read_Number_File($File_Name);
		### Append Number-File-Dictionary to Number-File-List
		$Number_File_List{$Number_File->{'Number'}} = Read_Number_File($File_Name);
	}
}

## Print all Number-Files
sub Print_Number_File_List()
{
	my $Number_File;

	foreach my $Number_File (sort {$a->{'Number'} <=> $b->{'Number'}} values %Number_File_List) {
		Print_Number_File($Number_File);
	}
}

## Test Number File
sub Number_File_List_Test()
{
	Read_Number_File_List();
	Print_Number_File_List();
}

Number_Reg_Exp_Test();
Name_Reg_Exp_Test();
Reference_Reg_Exp_Test();
Name_from_Reference_Reg_Exp_Test();
Number_File_List_Test();
