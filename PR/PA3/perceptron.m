function [ gc_funcs ] = perceptron(training_data)
%PERCEPTRON batch training
%   Generate discriminant functions based on Batch Perceptron
    
    % Step size alpha
    alpha = 1;
    
    % Fetch some info about training data
    n_classes = length(training_data);
    dim = size(training_data{1}, 2);
    
    % Construct discriminant functions for each pair of classes
    pairs = nchoosek(1:n_classes, 2);
    n_pairs = size(pairs, 1);
    
    % Initialize g_funcs array
    g_funcs = cell(1,n_pairs);
    
    % Initialize weights: a set of column vectors for each g_func
    a = zeros(dim + 1, n_pairs);
    
    % y(1) = 1, size(y) = dim + 1
    
    %figure
    %{
    hold
    plot(training_data{1}(:,1), training_data{1}(:,2), 'r.')
    plot(training_data{2}(:,1), training_data{2}(:,2), 'g.')
    plot(training_data{3}(:,1), training_data{3}(:,2), 'b.')
    %}
    
    % Train each classifier
    for i=1:n_pairs
        pair = pairs(i,:)
        
        % Initialize weights
        a = ones(dim + 1, 1);
        
        % Initialize set of misclassified examples
        y = [1];
        
        % Train while there still are misclassified examples
        while length(y) > 0
            % g(x) > 0 => correct classification
            g = @(x) a' * [1;x];
            
            
            %{
            a0 * 1 + a1 * x1 + a2 * x2 = 0
            x2 = -a1*x1/a2 - a0/a2
            %}
            %{
            x = -10:.1:20;
            
            f = @(x) -a(2) * x / a(3) - a(1)/a(3);
            plot(x, f(x), 'k-');
            %refreshdata
            drawnow
            %}
            
            y = [];
            
            % Classify!
            for j=pair
                % j is the target class
                %j
                for k=1:length(training_data{j})
                    x = training_data{j}(k,:);
                    
                    %if j == pair(2)
                        % Normalize
                    %    x = -x;
                    %end
                    
                    c = perceptron_classify(x', g, pair);
                    
                    %if g(x) <= 0
                    if c ~= j
                        % Misclassification, add to y
                        %printf('class %d: miss!\n', i);
                        if j == pair(2)
                            % Normalize
                            x = -x;
                        end
                        
                        y = [y;[1 x]];
                    end
                end
            end
            
            printf('%d misclassified...\n', length(y))
            %y
            % Update weights
            if length(y) > 0
                %printf('a:');
                %a
                %y
                %printf('sumy:');
                %sumy = sum(y)'
                %printf('update:');
                a = a + alpha * sum(y)';
            end
        end
        
        g_funcs{i} = g;
        
        %input('Continue?');
    end
    
    gc_funcs = cell(1, n_classes);
    
    for i=1:n_classes
        % i is target
        gc_funcs{i} = @(x) perceptron_vote(x, g_funcs, pairs, i);
    end
    %{
    def g(x, pairs, g_funcs, target):
        votes = 0
        for j in 1:n_pairs:
            pair = pairs(:,j)
            c = perceptron_classify(x, g_funcs{i}, pair)
            if c == target:
                votes += 1
            end
        end
        return c
            
    %}
end

function [ votes ] = perceptron_vote(x, g_funcs, pairs, target)
%PERCEPTRON vote
%   Calculate number of votes for class target based on two-category
%   discriminant functions g_funcs
    votes = 0;
    n_pairs = size(pairs, 1);
    
    for j=1:n_pairs
        pair = pairs(j,:);
        c = perceptron_classify(x, g_funcs{j}, pair);
        if c == target
            votes = votes + 1;
        end
    end
end

function [ c ] = perceptron_classify(x, g, pair)
%PERCEPTRON classify
%   classify x using discriminant function g
    if g(x) >= 0
        c = pair(1);
    else
        c = pair(2);
    end
end