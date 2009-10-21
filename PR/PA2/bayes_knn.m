function [probability]  = bayes_knn( class_data, x, k )
%   Use k-nearest neighbor to evalute class-conditional probabilities.
    
    %Create column full of the same datapoint with length equal to 
    %number of training points.
    dp_m = repmat(x, size(class_data, 1), 1);
        
    %Get the difference between the training points and the data point.
    diff_m = class_data - dp_m;
    %Now get the actual cartesian distances between all the points.
    dists = sort(sum(diff_m.^2, 2));
    %And the k closest points
    dists = dists(1:k);
    
    max_dist = max(dists);
    
    %Calculate the volume of the hypersphere of radius max_dist
    %Since we're always working with 2 dimensions here, we'll just hard
    %code it.
    
    V = pi * max_dist^2;
    
    %And the number of elements 
    N = length(class_data);
    
    probability = k / (N * V);
end

