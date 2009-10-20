function [ p ] = gmm( x, M, C, pi )
% GMM Gaussian Mixture Model
%   Computes p(x | M, C, pi)

    p = 0;
    for k=1:length(M)
        p = p + pi{k} * gaussian(x, M{k}, C{k});
    end

end

