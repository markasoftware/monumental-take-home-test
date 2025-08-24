% Minizinc to find a valid wild bond

%%%% PARAMETERS %%%%

int: n_courses;
set of int: COURSES = 1..n_courses;
int: width_in_quarters; % eg, if the width is 2 stretchers, then this would be 2*4 = 8
int: last_head_joint_index = width_in_quarters-2;
set of int: HEAD_JOINT_INDICES = 1..last_head_joint_index; % -2 to avoid left and right edges

%%%% DECISION VARLIABLES %%%%

% Which relative x-positions on each row have head joints (not including 0 or full-width).
% The decision to model possible head joints at every quarter brick on every course is not the only one.
% It's also possible to model possible head joints only every half-brick, but then you have to keep in mind
% the quarter-brick offset on every other row in the definition of all the other constraints later.
array[COURSES, HEAD_JOINT_INDICES] of var bool: head_joints;

%%%% OBJECTIVE %%%%

solve satisfy;

% If you wanted to "force" the bonds to be "more random", you could add an objective to minimize the
% difference between a provided, fully random bond (that may not satisfy the constraints) and the
% satisfying bond produced by the constraints in this file.

%%%% CONSTRAINTS %%%%

% Our head_joints array is modeled to allow joints at any quarter-brick position. However, the only
% actual quarter-bricks in the wild bond are at the left/right edges, so we need to constrain first
% where the valid head joint positions are
constraint forall(i in COURSES, j in HEAD_JOINT_INDICES where i mod 2 = j mod 2) (
    not head_joints[i, j]
);

% Ensure nothing larger than a stretcher, by saying that every stretcher-length segment has at least one head joint
constraint forall(i in COURSES, j in HEAD_JOINT_INDICES where j <= last_head_joint_index-4) (
    head_joints[i, j] \/ head_joints[i, j+1] \/ head_joints[i, j+2] \/ head_joints[i, j+3] \/ head_joints[i, j+4]
);

% No two half bricks next to each other
constraint forall(i in COURSES, j in HEAD_JOINT_INDICES where j+4<=last_head_joint_index) (
    not (head_joints[i, j] /\ head_joints[i, j+2] /\ head_joints[i, j+4])
);

% There's a lot of repetition in the next four constraints, which could be reduced. For example, in
% the diagonal constraints, we could do forall(k in 0..4) instead of explicitly listing out all five
% head joint positions. But I'll keep it repetitive for simplicitly instead.

% Prevent the vertical anti-pattern with initial movement to the left
constraint forall(i in COURSES, j in HEAD_JOINT_INDICES where i+4 <= n_courses /\ j >= 1 + 2) (
    not (
         head_joints[i, j]
               /\
         head_joints[i+1, j-1]
               /\
         head_joints[i+2, j]
               /\
         head_joints[i+3, j-1]
               /\
         head_joints[i+4, j]
     )
);

% Prevent the vertical anti-pattern with initial movement to the right
constraint forall(i in COURSES, j in HEAD_JOINT_INDICES where i+4<=n_courses /\ j <= last_head_joint_index-1) (
    not (
         head_joints[i, j]
               /\
         head_joints[i+1, j+1]
               /\
         head_joints[i+2, j]
               /\
         head_joints[i+3, j+1]
               /\
         head_joints[i+4, j]
     )
);

% Prevent the diagonal anti-pattern to the left
constraint forall(i in COURSES, j in HEAD_JOINT_INDICES where i+4<=n_courses /\ j >= 1 + 4) (
    not (
        head_joints[i, j]
              /\
        head_joints[i+1, j-1]
              /\
        head_joints[i+2, j-2]
              /\
        head_joints[i+3, j-3]
              /\
        head_joints[i+4, j-4]
    )
);

% Prevent the diagonal anti-pattern to the right
constraint forall(i in COURSES, j in HEAD_JOINT_INDICES where i+4<=n_courses /\ j <= last_head_joint_index-4) (
    not (
        head_joints[i, j]
              /\
        head_joints[i+1, j+1]
              /\
        head_joints[i+2, j+2]
              /\
        head_joints[i+3, j+3]
              /\
        head_joints[i+4, j+4]
    )
);