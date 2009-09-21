% Run classification tests on a dataset
% Parameters:
%   dataset - the dataset
%   class_offsets - offsets of class data in dataset
function [some_result] = run_tests(dataset, class_offsets)
    
    %
    % Set up data set
    %
    
    % Split data into N classes
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
    %plot(training_data{1}(:,1), training_data{1}(:,2), '.r', training_data{2}(:,1), training_data{2}(:,2), '.g')

    % Use 25% of data for testing
    test_data = {};
    for i=1:n_classes
        % Get number of elements in class:
        lim = floor(size(class_data{i}, 1) * 0.75);
        test_data{i} = class_data{i}(lim+1:end, :);
    end
    
    %plot(test_data{1}(:,1), test_data{1}(:,2), '.r', test_data{2}(:,1), test_data{2}(:,2), '.g' , test_data{3}(:,1), test_data{3}(:,2), '.b')

    
    %
    % Set up mean and covariance matrices
    %
    
    % Set up the mean cells.
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
        C_2a{i} = mean(diag(C_avg)) * eye(2);
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
    
    % 1a
    G_1a = bayes_generator(M, C_1a);
    [accuracy_1a, confusion_1a] = test_datasets(test_data, G_1a)
    plot_decision_region(training_data, G_1a);
    input('Hit ENTER to continue');
    
    % 1b
    G_1b = bayes_generator(M, C);
    [accuracy_1b, confusion_1b] = test_datasets(test_data, G_1b)
    plot_decision_region(training_data, G_1b);
    input('Hit ENTER to continue');
    
    % 2a
    G_2a = bayes_generator(M, C_2a);
    [accuracy_2a, confusion_2a] = test_datasets(test_data, G_2a)
    plot_decision_region(training_data, G_2a);
    input('Hit ENTER to continue');
    
    % 2b
    G_2b = bayes_generator(M, C_2b);
    [accuracy_2b, confusion_2b] = test_datasets(test_data, G_2b)
    plot_decision_region(training_data, G_2b);
    input('Hit ENTER to continue');
    
    % 2c
    G_2c = bayes_generator(M, C_2c);
    [accuracy_2c, confusion_2c] = test_datasets(test_data, G_2c)
    plot_decision_region(training_data, G_2c);
    input('Hit ENTER to continue');
    
    %hold
    %plot(result{1}(:,1), result{1}(:,2), '.y', result{2}(:,1),
    %result{2}(:,2), '.m')
end


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

function [] = plot_decision_region(training_data, g_funcs)
% PLOT_DECISION_REGION of g_funcs with training_data superposed
    
    % Concatenate all training data
    d = cat(1, training_data{:});
    
    % Calculate min and max for x and y
    mins = min(d);
    maxs = max(d);
    xmin = mins(1);
    ymin = mins(2);
    xmax = maxs(1);
    ymax = maxs(2);
    
    % Set up dimension of decision region image
    dim = 200;
    xstep = (xmax - xmin) / dim;
    ystep = (ymax - ymin) / dim;
    
    % Initialize decision region image
    img = zeros(dim);
    
    % Classify each point in img
    for i=1:dim
        for j=1:dim
            x = [xmin + i * xstep; ymin + j * ystep];
            img(j, i) = classify(x, g_funcs);
        end
    end
    
    % Set up color map for class 1, 2 and 3
    cmap = [0.8510 0.3647 0.2549; ...
            0.5647 0.6235 0.8118; ...
            0.4000 1.0000 0.4000];
    
    % Set up plot map for training data
    pmap = [0.6 0 0; 0 0 0.6; 0 0.7 0];
    
    % Apply color map and display image
    colormap(cmap)
    image([xmin xmax], [ymin ymax], img);
    axis xy
    hold
    
    % Plot training data
    for i=1:size(training_data, 2)
        plot(training_data{i}(:,1), training_data{i}(:,2), ...
            '.', 'MarkerEdgeColor', pmap(i,:));
    end
    hold
    
end
