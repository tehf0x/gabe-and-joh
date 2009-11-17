function [ result ] = categorize(dataset, classify, n_classes)
% CATEGORIZE a dataset using classifier
%   Returns an array for each class containing a matrix of features
    result = cell(1, n_classes);
    for i=1:size(dataset, 1)
        cls = classify(dataset(i,:)');
        
        if length(result) < cls
            result{cls} = [];
        end
        
        result{cls} = [result{cls}; dataset(i,:)];
    end
end

