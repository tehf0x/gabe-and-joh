function [ ind ] = classify( x, g_funcs )
    % Classify the feature vector x and return the class number
    num_classes = size(g_funcs);
    num_classes = num_classes(2);
    results = zeros(1,num_classes);
    for i=1:num_classes
        results(i) = g_funcs{i}(x);
    end
    [val, ind] = max(results);


