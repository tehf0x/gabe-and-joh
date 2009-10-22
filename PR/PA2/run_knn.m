function [ accuracy, confusion ] = run_knn( training_data, test_data, k )
%RUN_KNN Run trained KNN against test data

    % Create classifier function
    classify = knn_classify(training_data, k);

    % Concatenate test_data
    %td = cat(1, test_data{:});
    

    % Evaluate results
    [accuracy, confusion] = eval_classifier(test_data, classify);
end

