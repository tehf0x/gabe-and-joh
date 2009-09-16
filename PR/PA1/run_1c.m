% Load the dataset
dataset = load('Datasets/od_group14.txt');

% Offsets of class data in dataset
class_offsets = [500, 1000, 1500];

% Run the tests
run_tests(dataset, class_offsets)