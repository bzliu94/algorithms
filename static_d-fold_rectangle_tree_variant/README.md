2016-07-06

## explanation

we have almost a standard static d-fold rectangle tree, which balloons in terms of time for construction when we have high overlap due to number of recursive calls for middle trees. it is a variant because we construct d\_eff levels, with d\_eff = log base two of n and d\_eff <= d. for when we reach leaves of the tree during a query, i.e. when middle tree is size one (which we call a dead end), we do brute force intersection test. also, we perform "thinning", where we create lower level primary trees for a primary node about half the time, with the other time having brute force checking of set(p). in addition, we have re-using of lower level type-i trees (primary tree for set(p)) as lower level type-ii trees (primary tree for interval stored at p, since we have entries at internal nodes). further, we have re-using of type-ii trees for both endpoints of an interval in a middle tree. also, we have re-using of type-i trees for both endpoints of an interval in a middle tree if they come from set(p) interval collections that exactly match.

## usage

run using:

(from folder containing "core" folder)

python -m core.tree.StaticDFoldRectangleTree

python -m core.tree.count
