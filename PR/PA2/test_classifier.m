function [ ] = test_classifier( dataset, class_sizes, classify )
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

    % Split data into training and test-data
    [training_data, test_data] = generate_datasets(dataset, class_sizes);
    
    % Evaluate results
    [accuracy, confusion] = eval_classifier(test_data, classify);
    
    accuracy
    confusion
    
    % Plot decision region
    a = input('Plot decision region? ', 's');
    if a == 'y'
        plot_decision_region(training_data, classify);
    end
end

