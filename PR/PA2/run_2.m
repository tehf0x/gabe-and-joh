% Run tests for the KNN Classifier
printf('Parzen\n');

% NLS DATA
printf('\n NLS DATA:\n');
printf('\n Sphere \n');
dataset = load('datasets/nls_group14.txt');
% Sizes of classes in data set
class_sizes = [2446, 2447];
%Split it
[train, test] = generate_datasets(dataset, class_sizes);
test_classifier(train, test, parsen_classify(train, 5));

printf('\n Gauss\n');
% Sizes of classes in data set
class_sizes = [2446, 2447];
%Split it
[train, test] = generate_datasets(dataset, class_sizes);
test_classifier(train, test, parzen_normal_classify(train, 5));

%REAL DATA
printf('\n REAL DATA:\n');
printf('\n Sphere \n');
dataset = load('datasets/real/data.txt');
% Sizes of classes in data set
class_sizes = [2388, 2291, 2488];
[train, test] = generate_datasets(dataset, class_sizes);
test_classifier(train, test, parsen_classify(train, 1500));

%REAL DATA
printf('\n Gauss\n');
% Sizes of classes in data set
class_sizes = [2388, 2291, 2488];
[train, test] = generate_datasets(dataset, class_sizes);
test_classifier(train, test, parzen_normal_classify(train, 1500));