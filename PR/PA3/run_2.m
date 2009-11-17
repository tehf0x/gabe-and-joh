% BAYES with PCA

addpath('util');

load_d1;

% Run PCA on the data
training_data = pca(training_data, 1);
test_data = pca(test_data, 1);

%{
hold
%plot(training_data{1}(:,1), 'r.')
%plot(training_data{2}(:,1), 'g.')
%plot(training_data{3}(:,1), 'b.')

plot(training_data{1}(:,1), training_data{1}(:,2), 'r.')
plot(training_data{2}(:,1), training_data{2}(:,2), 'g.')
plot(training_data{3}(:,1), training_data{3}(:,2), 'b.')
%plot3(training_data{1}(:,1), training_data{1}(:,2), training_data{1}(:,3), 'r.')
%}

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