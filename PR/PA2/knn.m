function [idx, results]  = k_nn( training_classes, test_classes, k )
%Apply k-nearest neighbor to a dataset.
%   Try and sort data into 'num_classes' classes using the K-NN algorithm.
%   'training_classes' should be cells of data points, one cell per class
%   'test_data' should be a column-matrix of data points to be classified
%   'k' is the number of nearest neighbours to consider in k-nn
    
    %If we are getting a cell of all the test classes, then clump them
    %together into one big matrix.
    if iscell(test_classes)
        test_lump = cat(1, test_classes{:});
    %Otherwise it's directly data points, so just put them together.
    else
        test_lump = test_classes;
    end
    
    training_lump = cat(1, training_classes{:});
    num_classes = size(training_classes, 2);
    %The datapoints will get sorted into these various cells:
    results = cell(num_classes, 1);
    %The index of the last point classified.  This is used when classifying
    %only one point.
    idx = -1;
    
    %For each point in the training data, classify it based on the K nearest
    %neighbours
    for i = 1:size(test_lump, 1)
        %Cell of k distances from a point to each training class.
        distances = {};
        %The datapoint
        dp = test_lump(i, :);
        
        %For each class, calculate the k closest points
        for n = 1:num_classes
            %Create column full of the same datapoint with length equal to 
            %number of training points.
            dp_m = repmat(dp, size(training_classes{n}, 1), 1);
        
            %Get the difference between the training points and the data point.
            diff_m = training_classes{n} - dp_m;
            %Now get the actual cartesian distances between all the points.
            dists = sort(sum(diff_m.^2, 2));
            %And the k closest points
            distances{n} = dists(1:k);
        end
        
        %All the distances lumped together:
        dist_lump = sort(cat(1, distances{:}));
        dist_lump = dist_lump(1:k);
        %This will allow us to classify the point
        histogram = zeros(num_classes, 1);
        
        %For the first k distances, tally the histogram based on what class
        %the distance comes from.  If the same distance is present in 2
        %classes' distance matrices, both the classes will be awarded for
        %this.
        for d = 1:k
                %See what class the distance comes from.
                for n = 1:num_classes
                    idx = find(distances{n}==dist_lump(d));
                    %Increment the histogram
                    if(~isempty(idx))
                        histogram(n) = histogram(n) + 1;
                    end
                end
        end
        %And now attribute that data point to the class:
        [val, idx] = max(histogram);
        results{idx} = cat(1, results{idx}, dp);
    end
end

