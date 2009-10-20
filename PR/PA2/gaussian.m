function [ p ] = gaussian(x, M, C)
%GAUSSIAN Summary of this function goes here
%   Detailed explanation goes here

    d = size(x, 2);
    p = (1/((2*pi)^(d/2) * sqrt(det(C)))) * exp(-0.5 * (x - M)' * C^-1 * (x - M));

end

