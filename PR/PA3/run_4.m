% PERCEPTRON

addpath('util');

load_d2;

% Train perceptron
g_funcs = perceptron(training_data);
classify = discr_classify_gen(g_funcs);

% Test classifier
test_classifier(training_data, test_data, classify);
