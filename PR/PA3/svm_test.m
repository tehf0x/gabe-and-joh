function [ ] = svm_test(test_data, pair, filename)
%SVM_TEST Generate output for SVM testing with SVM Test
%
%   pair = which two classes to generate output
%   filename = output filename
%
%   Format is:
%       n_examples dim
%       x1 x2 ... xdim
%       ...

    fid = fopen(filename, 'w');
    
    t1 = test_data{pair(1)};
    t2 = test_data{pair(2)};
    
    n_examples = size(t1, 1) + size(t2, 1);
    dim = size(t1, 2);
    
    %fprintf(fid, '%d %d\n', n_examples, dim+1);
    fprintf(fid, '%d %d\n', n_examples, dim);
    
    for t=[t1;t2]'
        fprintf(fid, '%f %f\n', t(1), t(2));
    end
    
    %{
    for t=t1'
        fprintf(fid, '%f %f +1\n', t(1), t(2));
    end
    
    for t=t2'
        fprintf(fid, '%f %f -1\n', t(1), t(2));
    end
    %}
    
    printf('Wrote test examples to %s\n', filename);
    printf('Now run: svm_test -no -ae -am -oa <result.txt> <model.txt> %s\n', filename);

end

