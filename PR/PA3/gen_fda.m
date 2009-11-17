function [ g_funcs, weight_vectors ] = gen_fda( training_data )
%Generate the weight vector for Fisher Multiple Discriminant Analysis
%   Calculate the best W vector as described p123 DudaHart

    n_classes = size(training_data, 2);
    weight_vectors = {};
    l_funcs = {};
    pairs = nchoosek(1:n_classes,2);
    n_pairs = length(pairs);
    for i=1:n_pairs
        weight_vectors{i} = find_weight(training_data, pairs(i,:));
        [cutoff, direction] = calc_cutoff(weight_vectors{i}, training_data, pairs(i,:));
        l_funcs{i} = @(x) (weight_vectors{i} * x' - cutoff) * direction;
    end
    g_funcs = {};
    for i=1:n_classes
        g_funcs{i} = @(x) vote_classify(x', l_funcs, pairs, i);
    end
end

function [weight_vector] = find_weight(training_data, pair)
%Find the weight vector that maximizes J between class1 and class2.
    
    class1 = training_data{pair(1)};
    class2 = training_data{pair(2)};
    m_diff = (mean(class1) - mean(class2));
    S_w = (cov(class1) * (length(class1)-1)) + (cov(class2) * (length(class2)-1));
    weight_vector = (inv(S_w) * m_diff')';
end

function [cutoff, direction] = calc_cutoff(weight_vector, training_data, pair)
%Find the best cutoff between the 2 classes for the projection on this
%weight_vector.
    m1 = weight_vector * mean(training_data{pair(1)})';
    v1 = weight_vector * var(training_data{pair(1)})';
    m2 = weight_vector * mean(training_data{pair(2)})';
    v2 = weight_vector * var(training_data{pair(2)})';
    
    %cutoff = ((v2/v1)*m2 + (v1/v2)*m1) / 2;
    cutoff = (m2 + m1) /2;
    
    %Depends on which side of the cutoff m1 is:
    if(m1>m2)
        direction = 1;
    else
        direction = -1;
    end
end
