function [ g_funcs ] = gmm_generator(M,C,pi)
% Generate discriminant functions using GMMs
%   M = Cell of mixture means for each class
%   C = Cell of mixture covariances for each class
%   pi = Cell of mixture coefficients for each class
%
%   Returns an array of functions for each class
    
    % Check that stuff corresponds.
    num_classes = length(M);
    %a = size(C);
    
    %if (a ~= num_classes)
    %    fprintf('Means array size and covariance array size do not correspond!\n');
    %    return
    %end
    
    % Initialize g_funcs array
    g_funcs = {};
    
    % Create discriminant function for each class
    for i = 1:num_classes
        g_funcs{i} = @(x) gmm(x, M{i}, C{i}, pi{i});
    end
end

