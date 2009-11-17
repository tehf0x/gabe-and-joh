function [ model_files ] = svm_train(name, training_data)
%SVM_TRAIN Generate output for SVM training with SVM Torch
%
%   pair = which two classes to generate output
%   filename = output filename
%
%   Format is:
%       n_examples dim+1
%       x1 x2 ... xdim [+-]1
%       ...
    
    % SVM commands
    % 'svm_torch -ae -am -t 0 <train.txt> <model.txt>
    svm_torch = 'svm/svm_torch -ae -am -t 0 %s %s';
    
    % Fetch some info about training data
    n_classes = length(training_data);
    
    % Construct discriminant functions for each pair of classes
    pairs = nchoosek(1:n_classes, 2);
    n_pairs = size(pairs, 1);
    
    % Initialize l_funcs array
    l_funcs = cell(1,n_pairs);
    
    % Initialize model filename array
    model_files = cell(n_pairs, 1);
    
    % Iterate through each pair
    for i=1:n_pairs
        pair = pairs(i,:);
        
        filename = sprintf('svm/data/%s_train_%d-%d.txt', name, pair(1), pair(2));
        fid = fopen(filename, 'w');
        
        t1 = training_data{pair(1)};
        t2 = training_data{pair(2)};
        
        n_examples = size(t1, 1) + size(t2, 1);
        dim = size(t1, 2);
        
        fprintf(fid, '%d %d\n', n_examples, dim + 1);
    
        for t=t1'
            s = sprintf('%d ', t);
            fprintf(fid, '%s+1\n', s);
        end

        for t=t2'
            s = sprintf('%d ', t);
            fprintf(fid, '%s-1\n', s);
        end

        fclose(fid);
        
        printf('Wrote training examples to %s\n', filename);
        
        model_files{i} = sprintf('svm/data/%s_model_%d-%d.txt', name, pair(1), pair(2));
        cmd = sprintf(svm_torch, filename, model_files{i});
        
        printf('Running %s...\n', cmd);
        [status, output] = unix(cmd);
        
        if status ~= 0
            % Error occured
            printf('OH NO! An error occured!\n');
            printf('%s\n', output);
        end
        
        %l_funcs{i} = @(x) svm_test(x, models{i});
    end
    
    
    g_funcs = cell(1, n_classes);
    
    for i=1:n_classes
        % i is target
        g_funcs{i} = @(x) vote_classify(x, l_funcs, pairs, i);
    end
    
    
    %{
    fid = fopen(filename, 'w');
    
    t1 = training_data{pair(1)};
    t2 = training_data{pair(2)};
    
    n_examples = size(t1, 1) + size(t2, 1);
    dim = size(t1, 2);
    
    fprintf(fid, '%d %d\n', n_examples, dim + 1);
    
    for t=t1'
        fprintf(fid, '%f %f +1\n', t(1), t(2));
    end
    
    for t=t2'
        fprintf(fid, '%f %f -1\n', t(1), t(2));
    end
    
    printf('Wrote training examples to %s\n', filename);
    printf('Now run: svm_torch -ae -am -t 0 %s <model.txt>\n', filename);
    %}
end

function [ l ] = svm_test(x, model_file)
    % svm_test -no -ae -am -oa <result.txt> <model.txt> <test.txt>
    svm_test = 'svm/svm_test -no -ae -am -oa %s %s %s';
    
    % Write x to file...
    %   n_examples dim
    %   x1 x2 ... xdim
    
    test_file = 'svm/data/test.tmp.txt';
    fid = fopen(test_file, 'w');
    
    dim = length(x);
    fprintf(fid, '1 %d\n', dim);
    
    s = sprintf('%d ', x);
    fprintf(fid, '%s\n', s);
    
    fclose(fid);
    
    % Execute svm_test to get result
    result_file = 'svm/data/result.tmp.txt';
    cmd = sprintf(svm_test, result_file, model_file, test_file);
    
    %printf('Running %s...\n', cmd);
    
    [status, output] = unix(cmd);
    
    if status ~= 0
        % Error occured
        printf('OH NO! An error occured!\n');
        printf('%s\n', output);
    end
    
    % Load result file
    l = load(result_file);
end