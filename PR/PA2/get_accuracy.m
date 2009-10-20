function [accuracy, confusion] = get_accuracy(test_data, classified_data)
%Return the accuracy of the classified data based on the test data.

    num_classes = min(size(test_data))
    accuracies = {}
    for i=1:num_classes
        num_wrong = length(nonzeros(test_data{i} - classified_data{i}))
        accuracies{i} = 1 - num_wrong / length(test_data{i})
    end
    %This syntax is ugly, but oh well...
    accuracy = mean([accuracies{:}])

end