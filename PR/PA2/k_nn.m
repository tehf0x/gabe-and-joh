function [sorted_data]  = k_nn( training_classes, test_data, k )
%Apply k-nearest neighbor to a dataset.
%   Try and sort data into 'num_classes' classes using the K-NN algorithm.
%   'training_classes' should be cells of data points, one cell per class
%   'test_data' should be a column-matrix of data points to be classified
%   'k' is the number of nearest neighbours to consider in k-nn

num_classes = max(size(training_classes))
%For each point in the training data, classify it based on the K nearest
%neighbours
for ....
        

end

