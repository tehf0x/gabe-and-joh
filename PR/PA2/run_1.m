% Run tests for the GMM classifier

% NONLINEARLY SEPARABLE DATASET
printf('NONLINEARLY SEPARABLE DATASET\n');

% Load the dataset
dataset = load('datasets/nls_group14.txt');

% Sizes of classes in data set
class_sizes = [2446, 2447];

% Split data into training and test-data
[training_data, test_data] = generate_datasets(dataset, class_sizes);

% EITHER: Train the GMM (will take a long time)
%[Ms, Cs, pis, K] = train_gmm(training_data, 1);
% Store the result for later use
%save gmm_nls Ms Cs pis K

% OR: Load trained GMM parameters from file
load gmm_nls.mat

% a) Diagonal covariance matrix
printf('Diagonal covariance matrix:\n');
Cs_diag = Cs;
for c=1:length(Cs)
   for k=1:length(Cs{c})
       Cs_diag{c}{k} = diag(diag(Cs{c}{k}));
   end
end

[accuracy, confusion] = run_gmm(test_data, Ms, Cs_diag, pis)

% b) Full covariance matrix
printf('Full covariance matrix:\n');
[accuracy, confusion] = run_gmm(test_data, Ms, Cs, pis)



% REAL WORLD DATASET
printf('REAL WORLD DATASET\n');

% Load the dataset
dataset = load('datasets/real/data.txt');

% Sizes of classes in data set
class_sizes = [2388, 2291, 2488];

% Split data into training and test-data
[training_data, test_data] = generate_datasets(dataset, class_sizes);

% EITHER: Train the GMM (will take a long time)
%[Ms, Cs, pis, K] = train_gmm(training_data, 0.5);
% Store the result for later use
%save gmm_nls Ms Cs pis K

% OR: Load trained GMM parameters from file
load gmm_real.mat

% a) Diagonal covariance matrix
printf('Diagonal covariance matrix:\n');
Cs_diag = Cs;
for c=1:length(Cs)
   for k=1:length(Cs{c})
       Cs_diag{c}{k} = diag(diag(Cs{c}{k}));
   end
end

[accuracy, confusion] = run_gmm(test_data, Ms, Cs_diag, pis)

% b) Full covariance matrix
printf('Full covariance matrix:\n');
[accuracy, confusion] = run_gmm(test_data, Ms, Cs, pis)
