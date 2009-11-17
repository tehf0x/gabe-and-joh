% PERCEPTRON

addpath('util');

load_d2;

% Generate weight vectors
g_funcs = gen_fda(training_data);
classify = discr_classify_gen(g_funcs);

% Test classifier
test_classifier(training_data, test_data, classify);
