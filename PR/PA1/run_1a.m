% RUN tests for LINEARLY SEPARABLE data set

% Load the dataset
dataset = load('Datasets/ls_group14.txt');

% Offsets of class data in dataset
class_offsets = [500, 1000, 1500];

% Run the tests
run_tests(dataset, class_offsets)