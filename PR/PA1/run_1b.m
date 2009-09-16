% Load the dataset
dataset = load('Datasets/nls_group14.fixed.txt');

% Offsets of class data in dataset
class_offsets = [2446, 4893];

% Run the tests
run_tests(dataset, class_offsets)