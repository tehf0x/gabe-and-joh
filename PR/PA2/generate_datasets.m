function [ training_data, test_data] = generate_datasets( dataset, class_sizes )    
% Split dataset into training and test classes.
%   Split data into N classes, and take the first 75% as training, with the
%   remaining data as test data.
    n_classes = size(class_sizes, 2);
    class_data = {};
    offset = 1;
    for i=1:n_classes
        class_data{i} = dataset(offset:offset+class_sizes(i)-1,:);
        offset = offset + class_sizes(i);
    end
    
    %plot(class_data{1}(:,1), class_data{1}(:,2), '.r', class_data{2}(:,1), class_data{2}(:,2), '.g' , class_data{3}(:,1), class_data{3}(:,2), '.b')
    
    % Grab the lower 75% of each class for training data
    training_data = {};
    test_data = {};
    for i=1:n_classes
        % Get number of elements in class:
        lim = floor(size(class_data{i}, 1) * 0.75);
        training_data{i} = class_data{i}(1:lim, :);
        test_data{i} = class_data{i}(lim+1:end,:);
    end
end

