function [ Ms, Cs, pis ] = train_gmm( dataset, class_sizes )
%TRAIN_GMM Train Gaussian Mixture Model from dataset
%   Varies number of mixtures until a 100% classification
%   accuracy is achieved.
%
%   Returns the means, covariances and pis for the K mixtures
%   in each class.
    
    % Split data into training and test-data
    [training_data, test_data] = generate_datasets(dataset, [2446, 2447]);
    
    % Initialize K to 0
    K = 0;
    
    % Increase K until we achieve 100% classification accuracy
    accuracy = 0;
    while accuracy ~= 1
        K = K + 1;
        
        printf('Trying K=%d... ', K);
        
        Ms = {};
        Cs = {};
        pis = {};

        for c=1:length(training_data)
            [M, C, pi] = em_gmm(training_data{c}, K);
            Ms{c} = M;
            Cs{c} = C;
            pis{c} = pi;
        end
        
        % Evaluate the model
        printf('Evaluating... ');
        g_funcs = gmm_generator(Ms, Cs, pis);
        classify = discr_classify_gen(g_funcs);
        td = cat(1, test_data{:});
        result = categorize(td, classify);
        
        [accuracy, confusion] = eval_results(test_data, result);
        
        printf('%.2f%% accuracy\n', accuracy * 100);
    end
end
