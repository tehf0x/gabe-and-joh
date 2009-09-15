function [ ind ] = classify( x, g_funcs )
    %Classify the various features and return the percentage error for each
    %class.
    num_classes = size(g_funcs);
    num_classes = num_classes(2);
    results = zeros(1,num_classes);
    for i=1:num_classes
        results(i) = g_funcs{i}(x);
    end
    [val, ind] = max(results);


