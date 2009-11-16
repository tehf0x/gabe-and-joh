addpath('bayes');
load_d1;

% Set up the mean cells.
M = {};
for i=1:n_classes
    % Get the mean of the class
    M{i} = mean(training_data{i})';
end
    
% Set up the covariance matrix cells (1b)
C = {};
for i=1:n_classes
    % Get the mean of the class
    C{i} = cov(training_data{i})';
end

G = bayes_generator(M,C);

[accuracy, confusion] = test_datasets(test_data, G);

accuracy

print_confusion_latex(confusion)