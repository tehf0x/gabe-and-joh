function [ classifier ] = bayes_knn_classify( training_classes, k )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

    num_classes = length(training_classes);
    g_funcs = {};
    for i=1:num_classes
        g_funcs{i} = @(x) bayes_knn(training_classes{i}, x, k);
    end
    classifier = @(x) discr_classify(x', g_funcs);
end

