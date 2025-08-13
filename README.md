## Unit systems

For different purposes, we have two different unit systems: "logical" units which are decimals
relative to 220mm (one brick + one head joint), and then "real" units which are just mm.

You can't exactly convert "logical" units to "real" units, because logical units include the head joint following the brick, while real units are just for the brick itself. To convert logical to real:

real = logical * 220 - 10

So a 1.0 logical length brick (stretcher) has real length 210mm, a 0.5 logical length brick (header)
has real length 100mm, and a quarter brick has real length 45mm.

We generate the bonds in relative units. We also print bricks using their relative units, because
generating ascii art in "real" units would require a very wide terminal (for a head joint to be one
char, we'd have to use 10mm = 1 character which would mean a single stretcher is 21 chars wide!).
Using relative units, we can use a different ratio between brick / header length than IRL.
