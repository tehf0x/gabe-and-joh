function [ votes ] = vote_classify(x, l_funcs, pairs, target)
%Linear seperator vote
%   Calculate number of votes for class target based on two-category
%   discriminant functions l_funcs
    votes = 0;
    n_pairs = size(pairs, 1);
    
    for j=1:n_pairs
        pair = pairs(j,:);
        c = linear_classify(x, l_funcs{j}, pair);
        if c == target
            votes = votes + 1;
        end
    end
end

function [ c ] = linear_classify(x, g, pair)
%Linear classify
%   classify x using discriminant function g
    if g(x) >= 0
        c = pair(1);
    else
        c = pair(2);
    end
end