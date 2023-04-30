#!/bin/perl

sub quicksort {
    my @arr = @_;
    if (@arr <= 1) {
        return @arr;
    }
    my $pivot = $arr[int(@arr/2)];
    my @left = grep { $_ < $pivot } @arr;
    my @middle = grep { $_ == $pivot } @arr;
    my @right = grep { $_ > $pivot } @arr;
    return (quicksort(@left), @middle, quicksort(@right));
}

my @my_list = (4, 2, 7, 1, 3, 5, 6);
my @sorted_list = quicksort(@my_list);
print join(", ", @sorted_list), "\n";
