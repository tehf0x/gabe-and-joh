% BAYES

addpath('util');

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
classify = discr_classify_gen(G);

% Evaluate results
[accuracy, confusion] = eval_classifier(test_data, classify);

accuracy
confusion

% Latex
printf('Confusion LaTeX:\n');
print_confusion_latex(confusion);