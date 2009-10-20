function [ M, C, pi ] = em_gmm( xs, K )
% EM_GMM Expectation Maximization for GMM
%   xs = training data
%   K  = number of mixtures
%   M = means for the k mixtures
%   C = covariances for the K mixtures
%   pi = mixture coefficients for the K mixtures

    % Initialize
    alpha = 0.01;   % Convergence limit
    dim = size(xs, 2);
    n_samples = size(xs, 1);

    M = cell(K, 1);
    for k=1:K
       % Choose means uniformly from training data
       % TODO: Is this the best way?
       M{k} = xs(round((k-1)*n_samples/k + 1),:)';
    end

    C = cell(K, 1);
    for k=1:K
       C{k} = diag(ones(dim,1));
    end

    pi = cell(K, 1);
    for k=1:K
       pi{k} = 1;
    end

    % gamma(z_nk)
    g = cell(n_samples, 1);
    for n=1:n_samples
       g{n} = zeros(K,1);
    end

    % TODO: Loop EM until convergence
    ll_prev = 0;
    ld = alpha * 100;
    while abs(ld) > alpha
        % E step
        for n=1:n_samples
            mixtures = zeros(K, 1);
            for j=1:K
                mixtures(j) = pi{j} * gaussian(xs(n,:)', M{j}, C{j});
            end
            mixsum = sum(mixtures);
            for k=1:K
               g{n}(k) = mixtures(k) / mixsum;
            end
        end

        % M step
        %Mold = M;
        %Cold = C;
        %piold = pi;
        for k=1:K
            % Mean
            Nk = 0;
            for n=1:n_samples
               Nk = Nk + g{n}(k); 
            end

            M{k} = zeros(dim, 1);
            for n=1:n_samples
                M{k} = M{k} + g{n}(k) * xs(n,:)';
            end
            M{k} = M{k} * 1/Nk;
            
            % Covariance
            C{k} = zeros(dim);
            for n=1:n_samples
                C{k} = C{k} + g{n}(k) * (xs(n,:)' - M{k}) * (xs(n,:)' - M{k})';
            end
            C{k} = C{k} * 1/Nk;
            
            % PI
            pi{k} = Nk / n_samples;
            
            %sprintf('DELTAS_%d:', k)
            %Mold{k}-M{k}
            %Cold{k}-C{k}
            %piold{k}-piold{k}
            
            
        end
        
        % Check for convergence
        ll = 0;
        for n=1:n_samples
           ll = ll + log(gmm(xs(n,:)', M, C, pi)); 
        end
        
        ld = ll - ll_prev;
        
        %ll
        ld
        
        ll_prev = ll;
    end

end

