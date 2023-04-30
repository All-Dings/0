# Dings-Lib-Perl

=for comment
The Dings-Lib-Perl is a [Dings-Lib](300010000.md) in [Perl](9010001.md).
=cut

## Imports

use 5.010;
use strict;
use utf8;
use warnings;
use Cwd;

binmode(STDOUT, "encoding(UTF-8)");
use open ':std', ':encoding(UTF-8)';

## Directory containing the Markdown Files
my $Dings_Directory = getcwd;

## Regular-Expressions

my $Reg_Exp_Number_File = '\d+' . '.' . '\w+';
my $Reg_Exp_Name = '[' . '\"\=\?\!\:\(\)\#\-\w\s@' . ']' . '+';

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

### Get File-Extension
my $File_Extension_Reg_Exp = '.+' . '\.' . '(' . '[a-zA-Z]+' . ')' . '$';

sub File_Extension_Reg_Exp_Test()
{
	Reg_Exp_Test($File_Extension_Reg_Exp, 'test.pl');
	Reg_Exp_Test($File_Extension_Reg_Exp, 'test.py');
}

sub Get_File_Extension($)
{
	my $File_Path =$_[0];

	if ($File_Path !~ /$File_Extension_Reg_Exp/) {
		return "";
	} else {
		return $1;
	}
}

### Get Dings-Name From First-Line
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

### Get Number From Number-File
my $Number_Reg_Exp = '^' . '(' . '\d+' . ')' . '.md' . '$';

sub Number_Reg_Exp_Test()
{
	Reg_Exp_Test($Number_Reg_Exp, '0.md');
	Reg_Exp_Test($Number_Reg_Exp, '341324.md');
}

### Get Reference From Line
my $Reference_Reg_Exp = '(' . '\[' . $Reg_Exp_Name . '\]' . '\(' . $Reg_Exp_Number_File . '\)' . ')';

sub Reference_Reg_Exp_Test()
{
	Reg_Exp_Test($Reference_Reg_Exp, 'The Man [Michael-Holzheu](0.md) creates the Dings-Project.');
	Reg_Exp_Test($Reference_Reg_Exp, '[Michael-Holzheu](0.md) builds Dings-Project.');
	Reg_Exp_Test($Reference_Reg_Exp, 'The Digns-Prject is created by [Michael-Holzheu](0.md)');
	Reg_Exp_Test($Reference_Reg_Exp, 'Height is a [Dimension-Interval](10000021.md) for the [Altitude-Dimension](10000030.md).');
}

### Get Name From Reference
my $Name_From_Reference_Reg_Exp = '\[' . '(' . $Reg_Exp_Name . ')' . '\]' . '\(' . $Reg_Exp_Number_File . '\)';

sub Name_From_Reference_Reg_Exp_Test()
{
        Reg_Exp_Test($Name_From_Reference_Reg_Exp, '[Michael-Holzheu](0.md)');
}

### Get Number from Reference
my $Number_From_Reference_Reg_Exp = '\[' . $Reg_Exp_Name . '\]' . '\(' . '(' . '\d+' . ')' . '.' . '\w+' . '\)';
# my $Number_From_Reference_Reg_Exp = '\[.*\]' . '\(' . '(' . '\d+' . ')' . '.' . '\w+' . '\)';

sub Number_From_Reference_Reg_Exp_Test()
{
	Reg_Exp_Test($Number_From_Reference_Reg_Exp, '[Michael-Holzheu](0.md)');
}

## Number-File-List
my $Number_File_List = {};

## Print Number-File
sub Print_Number_File($)
{
	my $Number_File = $_[0];
	my $Name = $Number_File->{'Name'};
	my $Number = $Number_File->{'Number'};
	printf("%d \"%s\"\n", $Number, $Name);
	my $h = $Number_File->{'Target_References'};
	foreach my $Reference (sort {$a->{'Id'} <=> $b->{'Id'}} values %$h) {
		my $Source = $Reference->{'Source'};
		printf("  - $Reference->{'Name'} [$Source->{'Name'}]($Source->{'Number'})\n");
	}
}

## Remove White-Space From the Start and End of a String
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
	$Number_File->{'Source_References'} = {};
	$Number_File->{'Target_References'} = {};

	return $Number_File;
}

# Required for List-Simulation ;-)
my $Reference_Id = 0;

## Read References of a Number-File
sub Read_Number_File_References($)
{
	my ($Line, $Reference, $Target_Number, $Target_Name, $Target);
	my $File_Name = $_[0];

	$File_Name =~ /$Number_Reg_Exp/;
	my $Source_Number = $1;
	my $Source = $Number_File_List->{$Source_Number};

	open my $File, '<', $File_Name;
	while ($Line = <$File>)  {
		if ($Line !~ /$Reference_Reg_Exp/) {
			next;
		}
		$Reference = $1;
		$Reference =~ /$Number_From_Reference_Reg_Exp/;
		$Target_Number = $1;
		$Reference =~ /$Name_From_Reference_Reg_Exp/;
		$Target_Name = $1;

		if (!exists($Number_File_List->{$Source_Number})) {
			print STDERR "Source-Number $Source_Number not found.\n";
			next;
		}
		if (!exists($Number_File_List->{$Target_Number})) {
			print STDERR "Target-Number $Target_Number not found.\n";
			next;
		}
		$Target = $Number_File_List->{$Target_Number};
		$Reference = {};
		$Reference->{'Source'} = $Source;
		$Reference->{'Target'} = $Target;
		$Reference->{'Name'} = $Target_Name;
		$Reference->{'Id'} = $Reference_Id;
		$Source->{'Source_References'}{$Reference_Id} = $Reference;
		$Target->{'Target_References'}{$Reference_Id} = $Reference;;
		$Reference_Id++;
	}
	close $File;
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
		$Number_File_List->{$Number_File->{'Number'}} = Read_Number_File($File_Name);
	}
	foreach my $File_Name (@File_List) {
		if ($File_Name !~ /$Number_Reg_Exp/) {
			next;
		}
		Read_Number_File_References($File_Name)
	}
}

## Print all Number-Files
sub Print_Number_File_List()
{
	my $Number_File;

	foreach my $Number_File (sort {$a->{'Number'} <=> $b->{'Number'}} values %$Number_File_List) {
		Print_Number_File($Number_File);
	}
}

## Test Number File
sub Number_File_List_Test()
{
	Read_Number_File_List();
	Print_Number_File_List();
}

package Code_To_Markdown;

use constant {
	Init => 1,
	Code => 2,
	Comment => 3,
	Heading => 4,
};

sub new($)
{
	my $Class = $_[0];
	my $Self = {
		'State' => Init,
		'Reg_Exp_Heading' => '^' . '#+' . ' ' . '.*',
		'Reg_Exp_Comment' => '^' . '"""' . '\s*',
	};
	bless $Self, $Class;
	return $Self;
}

sub Process_End($)
{
	my $Self = $_[0];
	if ($Self->{State} == Code) {
		printf "```\n";
	}
}

sub Process_Line($$$$)
{
	my $Self = $_[0];
	my $Line = $_[1];
	my $Line_Number = $_[2];
	my $Language_Tag = $_[3];

	$Line =~ s/\s+$//;
	if (length($Line) == 0) {
		# Do nothing
	} elsif ($Self->{State} == Init) {
		if ($Line =~ /$Self->{Reg_Exp_Heading}/) {
			$Self->{State} = Heading;
			print "$Line\n";
		} elsif ($Line =~ /$Self->{Reg_Exp_Comment}/) {
			$Self->{State} = Comment;
		} else {
			print "```$Language_Tag\n";
			print "$Line\n";
			$Self->{State} = Code;
		}
	} elsif ($Self->{State} == Heading) {
		if ($Line =~ /$Self->{Reg_Exp_Heading}/) {
			print "$Line\n";
			$Self->{State} = Heading;
		} elsif ($Line =~ /$Self->{Reg_Exp_Comment}/) {
			$Self->{State} = Comment;
		} else {
			print "```$Language_Tag\n";
			print "$Line\n";
			$Self->{State} = Code;
		}
	} elsif ($Self->{State} == Code) {
		if ($Line =~ /$Self->{Reg_Exp_Heading}/) {
			print "```\n";
			print "$Line\n";
			$Self->{State} = Heading;
		} elsif ($Line =~ /$Self->{Reg_Exp_Comment}/) {
			print "```\n";
			$Self->{State} = Comment;
		} else {
			print "$Line\n";
			$Self->{State} = Code;
		}
	} elsif ($Self->{State} == Comment) {
		if ($Line =~ /$Self->{Reg_Exp_Comment}/) {
			$Self->{State} = Init;
		} else {
			print "$Line\n";
		}
	}
	return $Self->{State};
}

## Convert a Python-File into a Markdown-File
sub Convert($$)
{
	my $Self = $_[0];
	my $File_Path = $_[1];
	my $Line_Number = 1;
	my $Language_Tag;
	my $File_Extension = main::Get_File_Extension($File_Path);

	if ($File_Extension eq "py") {
		$Language_Tag = "python";
	} elsif ($File_Extension eq "pl") {
		$Language_Tag = "perl";
	} else {
		print STDERR "File-Type not supported: $File_Path\n";
		exit 1;
	}
	open my $File, '<', $File_Path;
	while (my $Line = <$File>)  {
		$Self->Process_Line($Line, $Line_Number, $Language_Tag);
	}
	$Self->Process_End();
}

package main;

sub Language_To_Markdown_Test()
{
	my $To_Markdown = new Code_To_Markdown();
	$To_Markdown->Convert("$Dings_Directory/300010010.py");
	$To_Markdown->Convert("$Dings_Directory/300010011.pl");
}

File_Extension_Reg_Exp_Test();
Language_To_Markdown_Test();
Number_From_Reference_Reg_Exp_Test();
Name_From_Reference_Reg_Exp_Test();
Number_Reg_Exp_Test();
Name_Reg_Exp_Test();
Reference_Reg_Exp_Test();
Name_From_Reference_Reg_Exp_Test();
Read_Number_File_List();
Print_Number_File_List();
