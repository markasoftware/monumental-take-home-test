% Minizinc to optimize assignment of bricks to strides

%%%% PARAMETERS %%%%

int: n_bricks; % The total number of bricks to be placed.
set of int: BRICKS = 1..n_bricks;

% dependency[i, j] is true if brick i must be placed before brick j.
array[BRICKS, BRICKS] of bool: dependency;

% within_stride[i, j] is true if brick i and j are close enough to be
% placed in the same stride.
array[BRICKS, BRICKS] of bool: within_stride;

%%%% DECISION VARIABLES %%%%

% which stride each brick is assigned to
array[BRICKS] of var 1..n_bricks: stride;

%%%% OBJECTIVE %%%%

solve minimize max(stride);

%%%% CONSTRAINTS %%%%

% Ensure all dependency bricks are in the same or previous stride
constraint forall(i, j in BRICKS where dependency[i, j]) (
    stride[i] <= stride[j]
);

% Ensure all bricks in a stride are close enough to be in a stride
constraint forall(i, j in BRICKS where i < j) (
    % arrow -> is implication
    (stride[i] == stride[j]) -> within_stride[i, j]
);