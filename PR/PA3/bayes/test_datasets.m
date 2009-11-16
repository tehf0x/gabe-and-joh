function [accuracy, confusion] = test_datasets(datasets, g_funcs)
% TEST_DATASETS returns accuracy and confusion matrix
    n_classes = size(g_funcs, 2);
    
    confusion = zeros(n_classes, n_classes);
    accuracy = zeros(n_classes, 1);
    
    for i=1:n_classes
        result = categorize(datasets{i}, g_funcs);
        for j=1:n_classes
            confusion(i, j) = size(result{j}, 1);
        end
        
        %plot(result{i}(:,1), result{i}(:,2), '.y')
        accuracy(i) = size(result{i}, 1) / size(datasets{i}, 1);
    end
    
    accuracy = mean(accuracy);
end