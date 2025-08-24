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

## Demo videos

Solving original problem as stated (stretcher bond, 2300x2000mm):

[original-problem.webm](https://github.com/user-attachments/assets/772801c4-a33d-4f66-ad9c-842ec167eee8)

Wild bond:

[wild-bond.webm](https://github.com/user-attachments/assets/33a8f49a-bdda-40dc-b337-f3e0feb82865)

## Installation & Running

### Debian/Ubuntu/other `apt` distros

From a Bash shell on the latest LTS Ubuntu or Debian (I tested in a `ubuntu:latest` docker container):

```bash
apt-get install -y minizinc python3 python3-pip python3-venv git
git clone https://github.com/markasoftware/monumental-take-home-test
cd monumental-take-home-test
python3 -m venv .venv
source .venv/bin/activate
pip install -g minizinc
```

Then you can run `python3 main.py <OPTIONS>` to run my submission.

To run the original problem as stated (2300x2000mm):

```
python3 main.py --num-courses 32 --width 10.5
```

### NixOS

After cloning and entering the cloned repo:

```
nix-shell -p python312 minizinc uv --command 'uv run main.py <OPTIONS>'
```

And like in the Ubuntu case, run with `--num-courses 32 --width 10.5` to run the problem as stated (2300x2000mm).

### Elsewhere

1. Install Python 3.12+ (older versions *might* work too)
2. Install Minizinc. It's in the package managers for most repos.
3. Install the `minizinc` Python package.
4. Run `main.py` under Python, passing extra command line arguments.

If you want, install the `uv` package manager, and then you can just do `uv run main.py` and skip step (3) above.

Use `--help` to learn about all the options.

And like in the Ubuntu case, run `main.py` with `--num-courses 32 --width 10.5` to run the problem as stated (2300x2000mm).

## Unit systems

For different purposes, we have two different unit systems: "logical" units which are decimals
relative to 220mm (one brick + one head joint), and then "real" units which are just mm.

You can't convert "logical" units to "real" units without more context, because of the head joints.
In some cases you will want to convert the real units including the head joint following the brick,
and sometimes not. To compute the width of a single brick (not including the trailing head joint):

```
real_brick_width = logical_brick_width * 220 - 10
```

So a 1.0 logical length brick (stretcher) has real length 210mm, a 0.5 logical length brick (header)
has real length 100mm, and a quarter brick has real length 45mm.

And of course, to convert logical units to real units including trailing head joint, just add 10mm.

We generate the bonds in relative units. We also print bricks using their relative units, because
generating ascii art in "real" units would require a very wide terminal (for a head joint to be one
char, we'd have to use 10mm = 1 character which would mean a single stretcher is 21 chars wide!).
Using relative units, we can use a different ratio between brick / header length than IRL.
