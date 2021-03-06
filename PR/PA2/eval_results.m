function [accuracy, confusion] = eval_results(test_data, classified_data)
%Return the accuracy of the classified data based on the test data.

    num_classes = length((test_data));
    accuracies = {};
    for i=1:num_classes
        num_wrong = size(setdiff(test_data{i}, classified_data{i}, 'rows'), 1);
        accuracies{i} = 1 - num_wrong / length(test_data{i});
    end
    
    %This syntax is ugly, but oh well...
    accuracy = mean([accuracies{:}]);

    confusion = zeros(num_classes);
    for i=1:num_classes
       for j=1:num_classes
           confusion(i,j) = length(test_data{i}) - size(setdiff(test_data{i}, classified_data{j}, 'rows'), 1);
    end
end