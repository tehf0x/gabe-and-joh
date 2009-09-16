% Run classification tests on a dataset
% Parameters:
%   dataset - the dataset
%   class_offsets - offsets of class data in dataset
function [your_mom] = run_tests(dataset, class_offsets)
    %plot(dataset(:,1), dataset(:,2), '.r')

    % Split data into 3 classes
    n_classes = size(class_offsets, 2);
    class_data = {};
    offset = 1;
    for i=1:n_classes
        class_data{i} = dataset(offset:class_offsets(i),:);
        offset = 1 + class_offsets(i);
    end
    
    %plot(class_data{1}(:,1), class_data{1}(:,2), '.r', class_data{2}(:,1), class_data{2}(:,2), '.g' , class_data{3}(:,1), class_data{3}(:,2), '.b')
    
    % Grab the lower 75% of each class for training data
    training_data = {};
    for i=1:n_classes
        % Get number of elements in class:
        lim = floor(size(class_data{i}, 1) * 0.75);
        training_data{i} = class_data{i}(1:lim, :);
    end
    
    %plot(training_data{1}(:,1), training_data{1}(:,2), '.r', training_data{2}(:,1), training_data{2}(:,2), '.g' , training_data{3}(:,1), training_data{3}(:,2), '.b')

    % Use 25% of data for testing
    test_data = {};
    for i=1:n_classes
        % Get number of elements in class:
        lim = floor(size(class_data{i}, 1) * 0.75);
        test_data{i} = class_data{i}(lim+1:end, :);
    end
    
    %plot(test_data{1}(:,1), test_data{1}(:,2), '.r', test_data{2}(:,1), test_data{2}(:,2), '.g' , test_data{3}(:,1), test_data{3}(:,2), '.b')

    % Set up the means cells.
    M = {};
    for i=1:n_classes
        % Get the mean of the class
        M{i} = mean(training_data{i})';
    end
    
    % Set up the covariance matrix cells (1b)
    C = {};
    for i=1:n_classes
        % Get the mean of the class
        C{i} = cov(training_data{i})';
    end

    % Set up an average covariance matrix needed for some of the problems
    C_avg = zeros(2);
    for i=1:4
        m = ones(1, n_classes);
        for t=1:n_classes
            m(t) = C{t}(i);
        end
        C_avg(i) = mean(m);
    end
    
    % Set up covariance cell where each covariance is C_avg (1a)
    C_1a = {};
    for i=1:n_classes
        C_1a{i} = C_avg;
    end
    
    % Naive Bayes -> features independent
    
    % C is same and is σ^2 * I (2a)
    % We estimate σ^2 by the average of the diagonal of C_avg
    C_2a = {};
    for i=1:n_classes
        C_2a{i} = mean(diag(C_avg)) * eye(n_classes);
    end
    
    % C is same and is C (2b)
    C_2b = {};
    for i=1:n_classes
        C_2b{i} = diag(diag(C_avg));
    end
    
    % C for each class is different (2c)
    C_2c = {};
    for i=1:n_classes
        C_2c{i} = diag(diag(C{i}));
    end
    
    
    %
    % Start tests
    %
    G_1a = bayes_generator(M, C_1a);
    classify(test_data{3}(1,:)', G_1a)
    
    
end