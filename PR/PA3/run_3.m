% PERCEPTRON

addpath('util');

load_d3;

% Generate weight vectors
g_funcs = gen_fda(training_data);
classify = discr_classify_gen(g_funcs);

% Evaluate results
[accuracy, confusion] = eval_classifier(test_data, classify);

accuracy
confusion

% Latex
printf('Confusion LaTeX:\n');
print_confusion_latex(confusion);


% Test classifier
%If we're not in 45 dimensions
%test_classifier(training_data, test_data, classify);
