function [ result ] = categorize(dataset, classify)
% CATEGORIZE a dataset using classifier
%   Returns an array for each class containing a matrix of features
    result = {};
    for i=1:length(dataset)
        cls = classify(dataset(i,:)');
        
        if length(result) < cls
            result{cls} = [];
        end
        
        result{cls} = [result{cls}; dataset(i,:)];
    end
end

