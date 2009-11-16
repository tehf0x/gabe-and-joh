function [ g_funcs ] = bayes_generator(M,C)
% Generate discriminant functions with mean M and covariance matrix C
%   Returns an array of functions for each class
    
    % Check that stuff corresponds.
    num_classes = size(M, 2);
    a = size(C);
    
    if (a ~= num_classes)
        fprintf('Means array size and covariance array size do not correspond!\n');
        return
    end
    
    % Initialize g_funcs array
    g_funcs = {};
    
    % Create discriminant function for each class
    for i = 1:num_classes
        W_i = -0.5 * inv(C{i});
        w_i = inv(C{i}) * M{i};
        % Ignore the prior probabilities, so the last log term is removed
        w_i0 = -0.5 * M{i}' * inv(C{i}) * M{i} - 0.5 * log(det(C{i}));
        g_funcs{i} = @(x) x' * W_i * x + w_i' * x + w_i0;
    end
end

