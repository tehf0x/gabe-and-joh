%Run the tests for the bayesian classifier on the 45-d dataset.
class_data = cell(0);
class_data{1} = load('datasets/real/class2_AlaskanWildlife.txt');
class_data{2} = load('datasets/real/class5_WildlifeGalapagos.txt');
class_data{3} = load('datasets/real/class6_NorthAmericanDeer.txt');

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
