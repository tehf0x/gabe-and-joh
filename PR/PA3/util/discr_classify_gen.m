function [ classifier ] = discr_classify_gen( g_funcs )
%DISCRIMINANT_CLASSIFY Generate a classifier based on discriminants
%   g_funcs should be a cell of discriminant functions
    
    classifier = @(x) discr_classify(x, g_funcs);
end

