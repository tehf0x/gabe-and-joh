% Load the dataset
dataset = load('Datasets/real_world/class.txt');

% Offsets of class data in dataset
class_offsets = [2388, 4679, 7167];

% Run the tests
run_tests(dataset, class_offsets)