function [ g_funcs ] = bayes_b(D,M,C)
    %Classify data based on some discriminant functions.
    %
    %Check that stuff corresponds.
    s = size(M);
    num_classes = s(2);
    a = size(C);
    %c_func = @(M) [m, n] = size(M), if m~=n, fprintf('Covariance matrix is not square!\n');, return, end
    if(a ~= num_classes)
        fprintf('Means array size and covariance array size do not correspond!\n');
        return
    end
    fprintf('Number of classes: %d\n', num_classes);
    %Initialize some variables:
    g_funcs = {};
    %Actual program code:
    
    for i = 1:num_classes
        W_i = -0.5 * inv(C{i})
        w_i = inv(C{i}) * M{i}
        %Ignore the prior probabilities, so the last log term is removed
        w_i0 = -0.5 * M{i}' * inv(C{i}) * M{i} - 0.5 * log(det(C{i})) 
        g_funcs{i} = @(x) x' * W_i * x + w_i' * x + w_i0
    end
end

