function [ ] = svm_train(training_data, pair, filename)
%SVM_TRAIN Generate output for SVM training with SVM Torch
%
%   pair = which two classes to generate output
%   filename = output filename
%
%   Format is:
%       n_examples dim+1
%       x1 x2 ... xdim [+-]1
%       ...

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

end

