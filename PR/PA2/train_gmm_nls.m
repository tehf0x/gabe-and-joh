% TRAIN GMM for NONLINEARLY SEPARABLE data set

% Load the dataset
dataset = load('datasets/nls_group14.txt');

% Sizes of classes in data set
class_sizes = [2446, 2447];

% Train the GMM
[Ms, Cs, pis] = train_gmm(dataset, class_sizes);

% Store the result for later use
save gmm_nls Ms Cs pis