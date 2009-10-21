function [ accuracy, confusion ] = run_gmm( test_data, Ms, Cs, pis )
%RUN_GMM Run trained GMM against test data

    % Create classifier function
    g_funcs = gmm_generator(Ms, Cs, pis);
    classify = discr_classify_gen(g_funcs);

    % Concatenate test_data
    td = cat(1, test_data{:});
    result = categorize(td, classify);

    % Evaluate results
    [accuracy, confusion] = eval_results(test_data, result);
end

