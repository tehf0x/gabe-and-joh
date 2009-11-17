%Run the tests for the bayesian classifier on the 2d linearly seperable
%dataset
dataset = load('datasets/ls_group14.txt');
class_offsets = [500,1000,1500];

% Split data into N classes
n_classes = size(class_offsets, 2);
class_data = {};
offset = 1;
for i=1:n_classes
    class_data{i} = dataset(offset:class_offsets(i),:);
    offset = 1 + class_offsets(i);
end

n_classes = 3;
% Grab the lower 75% of each class for training data
training_data = {};
for i=1:n_classes
    % Get number of elements in class:
    lim = floor(size(class_data{i}, 1) * 0.75);
    training_data{i} = class_data{i}(1:lim, :);
end
   
% Use 25% of data for testing
test_data = {};
for i=1:n_classes
    % Get number of elements in class:
    lim = floor(size(class_data{i}, 1) * 0.75);
    test_data{i} = class_data{i}(lim+1:end, :);
end
