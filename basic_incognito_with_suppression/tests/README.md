#pre-sets

note that pre-sets are for single-attribute generalization structures

A: divide into parts based on hyphens; levels are: 
   ungeneralized, censor n' parts for 0 < n' < n from right to left, 
   only first character unasterisked, fully suppressed; 
   n + 2 levels

takes an integer parameter n

B: ungeneralized, censor last 0 < n' < n characters 
   (allowing for variable length) from right to left, 
   fully suppressed; allow empty as a value; 
   n + 2 levels

takes a "True"/"False" parameter for doubling generalization costs

takes an optional integer parameter n describing max. prefix size

C: ungeneralized, fully suppressed; allow empty as a value; 
   two levels

D: digit right-to-left generalization with left-padding using zeroes; can deal with values longer than parameter digit count; m + 1 levels

   takes an num. digits integer parameter m

G: fully suppressed; allow empty as a value; 1 level

#input format

    <path to csv>
    <do output num. suppressed tuples line and suppressed row 1-indexed indices line; 0 for no, 1 for yes>
    <num. of header lines to ignore and carry over>
    <k>
    <suppression budget>
    <num. attributes>
    <num. quasi-identifier attributes>
    <line for 0th quasi-identifier attribute>
    ...
    <line for last quasi-identifier attribute>

where

    <line for ith quasi-identifier attribute>

is

    <index for quasi-identifier column> <capital pre-set type letter> <optional parameter for pre-set>

and

    <do output num. suppressed tuples line and ... >

refers to last two lines

#given test inputs

* airsampling - has four quasi-identifiers; for k = 2 and ~1/10 suppression budget (1024), takes ~2 min. 24 seconds to finish
* hospital - has nine quasi-identifiers; for k = 20 and ~1/10 suppression budget (453), takes ~45 min. and 37 seconds to finish 
* whitehouse - has three quasi-identifiers; for k = 124 and ~1/10 suppression budget (13416), takes ~12.1 seconds to finish
