function [ ] = test_classifier( dataset, class_sizes, classify )
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

    % Split data into training and test-data
    [training_data, test_data] = generate_datasets(dataset, class_sizes);
    
    % Concatenate test_data
    td = cat(1, test_data{:});
    result = categorize(td, classify);

    % Evaluate results
    [accuracy, confusion] = eval_results(test_data, result);
    
    accuracy
    confusion
    
    % Plot decision region
    a = input('Plot decision region? ', 's');
    if a == 'y'
        plot_decision_region(training_data, classify);
    end
end

