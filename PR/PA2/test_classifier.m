function [ ] = test_classifier( training_data, test_data, classify )
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

    % Evaluate results
    [accuracy, confusion] = eval_classifier(test_data, classify);
    
    accuracy
    confusion
    
    % Latex
    printf('Confusion LaTeX:\n');
    print_confusion_latex(confusion);
    
    % Plot decision region
    a = input('Plot decision region? ', 's');
    if a == 'y'
        plot_decision_region(training_data, classify);
    end
end

