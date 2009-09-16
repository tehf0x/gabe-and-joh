function [ result ] = categorize(dataset, g_funcs)
% CATEGORIZE a dataset using g_funcs as the discriminant functions
    result = cell(1, size(g_funcs, 2));
    for i=1:size(dataset, 1)
        cls = classify(dataset(i,:)', g_funcs);
        result{cls} = [result{cls};dataset(i,:)];
    end
end

