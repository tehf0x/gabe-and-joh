function [accuracy, confusion] = eval_svm(test_data, model_files)
% NO COMMENTS!
    n_classes = length(test_data);

    confusion = zeros(n_classes, n_classes);
    accuracy = zeros(n_classes, 1);

    for i=1:n_classes
        result = svm_test(test_data{i}, n_classes, model_files);
        for j=1:n_classes
            confusion(i, j) = histc(result, j);
        end

        %plot(result{i}(:,1), result{i}(:,2), '.y')
        accuracy(i) = confusion(i, i) / sum(confusion(i,:));
    end

    accuracy = mean(accuracy);
end