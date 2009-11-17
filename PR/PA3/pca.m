function [ new_data ] = pca(data, new_dim)
%PCA Perform Principal Component Analysis on data
%   Reduces dimention of data to new_dim based on PCA
    
    n_classes = length(data);
    
    % Concatenate classes
    d = [];
    for k=1:n_classes
       d = [d;data{k}];
    end
    
    % Length of data
    [l,dim] = size(d);
    
    % Calculate mean and scatter matrix
    m = mean(d);
    S = cov(d) * (l-1);
    
    % Calculage eigenvalues D (diag) and eigenvectors V (columns)
    [V,D] = eig(S);
    
    % Extract new_dim eigenvectors
    e = V(:,dim-new_dim+1:dim);
    
    % Project into new_dim space!
    new_data = cell(1, length(data));
    for k=1:n_classes
        dk = data{k};
        l = size(dk,1);
        new_data{k} = zeros(l, new_dim);
        for i=1:l
            xi = dk(i,:);
            for j=1:new_dim
                new_data{k}(i,j) = (xi - m) * e(:,j);
            end
        end
    end
end
