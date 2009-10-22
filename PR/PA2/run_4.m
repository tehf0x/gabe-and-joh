% Run tests for the KNN Classifier
printf('KNN\n');

% NLS DATA
printf('\n NLS DATA:\n');
dataset = load('datasets/nls_group14.txt');
% Sizes of classes in data set
class_sizes = [2446, 2447];
%Split it
[training_data, test_data] = generate_datasets(dataset, class_sizes);
[acc, confusion] = run_knn(training_data, test_data, 1);
%acc;
%print_confusion_latex(confusion);

%REAL DATA
printf('\n REAL DATA:\n');
dataset = load('datasets/real/data.txt');
% Sizes of classes in data set
class_sizes = [2388, 2291, 2488];
[training_data, test_data] = generate_datasets(dataset, class_sizes);
[acc, confusion] = run_knn(training_data, test_data, 60);
acc
print_confusion_latex(confusion)