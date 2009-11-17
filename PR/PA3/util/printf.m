function [ ] = printf( varargin )
%PRINTF Print formatted strings to stdout
    fprintf(1, varargin{:});
end

