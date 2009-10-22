function [ Ms, Cs, pis, K ] = train_gmm( training_data, target_accuracy )
%TRAIN_GMM Train Gaussian Mixture Model from dataset
%   Varies number of mixtures until a target_accuracy% classification
%   accuracy is achieved.
%
%   Returns the means, covariances and pis for the K mixtures
%   in each class.
    
    % Initialize K to 0
    K = 0;
    
    % Increase K until we achieve the target classification accuracy
    accuracy = 0;
    while accuracy < target_accuracy
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
        
        [accuracy, confusion] = eval_classifier(training_data, classify);
        
        printf('%.2f%% accuracy\n', accuracy * 100);
    end
end
