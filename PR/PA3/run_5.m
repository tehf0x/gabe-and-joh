% SVM

addpath('util');

% a. 45-dimensional representation of image data
printf('\n\n45 DIMENTIONAL:\n\n');

load_d1;

model_files = svm_train('d1', training_data);

[accuracy, confusion] = eval_svm(test_data, model_files)

% Latex
printf('Confusion LaTeX:\n');
print_confusion_latex(confusion);

input('Hit ENTER to continue');


% b. Reduced dimension representation of image data obtained using PCA

% Run PCA on the data

printf('\n\nPCA 45 DIMENTIONAL:\n\n');

load_d1;

training_data = pca(training_data, 1);
test_data = pca(test_data, 1);

model_files = svm_train('d1_pca', training_data);

[accuracy, confusion] = eval_svm(test_data, model_files)

% Latex
printf('Confusion LaTeX:\n');
print_confusion_latex(confusion);

input('Hit ENTER to continue');





% c. Linearly separable data
printf('\n\nLINEARLY SEPARABLE DATA:\n\n');

load_d2;

model_files = svm_train('d2', training_data);

[accuracy, confusion] = eval_svm(test_data, model_files)

% Latex
printf('Confusion LaTeX:\n');
print_confusion_latex(confusion);

% Plot decision region
a = input('Plot decision region? ', 's');
if a == 'y'
    svm_plot_decision_region(training_data, model_files);
end


% d. Overlapping data

printf('OVERLAPPING DATA:\n\n');

load_d3;

model_files = svm_train('d3', training_data);

[accuracy, confusion] = eval_svm(test_data, model_files)

% Latex
printf('Confusion LaTeX:\n');
print_confusion_latex(confusion);

% Plot decision region
a = input('Plot decision region? ', 's');
if a == 'y'
    svm_plot_decision_region(training_data, model_files);
end





