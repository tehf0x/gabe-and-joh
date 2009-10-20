function [ ind ] = discriminant_classify( x, g_funcs )
% CLASSIFY the feature vector x 
%   Returns the class number
    num_classes = size(g_funcs, 2);
    results = zeros(1, num_classes);
    for i=1:num_classes
        results(i) = g_funcs{i}(x);
    end
    [val, ind] = max(results);


