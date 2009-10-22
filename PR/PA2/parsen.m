function [ probability ] = parsen( class_data, x, h )
%Apply parsen window technique to calculate the P(x|w)
%   Pass in the training class, the data point, and h, the size of the
%   parsen window.  P(x|w) will be returned.
%   Note: if h is too small, it may not find any points within the
%   hypersphere and P(x|w) will be 0.

    %Create column full of the same datapoint with length equal to 
    %number of training points.
    dp_m = repmat(x, size(class_data, 1), 1);
    
    %Get the difference between the training points and the data point.
    diff_m = class_data - dp_m;
    %Now get the actual cartesian distances between all the points.
    dists = sort(sum(diff_m.^2, 2));
    %And the points within the hypersphere of radius h
    sphere_points = find(dists<=h);
    
    %Find out the number of elements that are within 
    k = length(sphere_points);
    %Calculate the volume of the hypersphere of radius max_dist
    %Since we're always working with 2 dimensions here, we'll just hard
    %code it.
    V = pi * h^2;
    
    %And the number of elements 
    N = length(class_data);
    
    probability = k / (N * V);
end

