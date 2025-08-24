## Overview

The main "cool" thing about my solution is that it uses a constraint solver (minizinc + gecode) to
optimize the distribution of bricks into different strides. There are probably some simple
algorithms that generate acceptable stride choices, but especially because of edge effects near the
top, bottom, left, and right I doubt that any simple and fast algorithm will come up with the
optimal stride selection. This is partially validated by the fact that, for larger walls, the solver
runs for a long time, and the solutions it comes up are not trivial or regular-looking.

My solution implements both the "bonus" parts of the problem. It supports the stretcher bond,
flemish bond, cross bond, and wild bond. To compute the wild bond, I also use a constraint solver.

As a result of using a constraint solver, my code can take a while to run. For the wall size
specified in the problem (2300x2000mm), the solver will run for a very long time if you let it. My
solution implements a default time limit of 20 seconds for the solver, which on my machine is long
enough to find a pretty good, nontrivial solution. In my opinion, it's better to find a more optimal
solution rather than to go fast; if it takes an extra few seconds to save multiple strides, you're
actually saving time at the end of the day.

## Installation/running

I used Python so that the interviewers will have an easy time reading my code, and because Python
has a good library for working with Minizinc, which I use as a frontend to constraint solvers.

The `main.py` file is the entry point. The `minizinc` python package is the only dependency. I'll
describe using `uv`, but you can install `minizinc` some other way if you'd like.

I recommend running with the `uv` package manager. Learn how to install it at
https://docs.astral.sh/uv (most Linux distros have `uv` in their repos these days, so eg `apt
install uv`)

Once you have `uv` installed:

```
uv run main.py <OPTIONS>
```

Use `--help` to learn about all the options.

The default options use a smaller wall size so that it goes fast. To run according to the problem
description (2300x2000mm stretcher bond):

```
uv run main.py --num-courses 32 --width 10.5
```

(as described below, width is measured in relative units).

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
