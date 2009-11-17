function [] = plot_decision_region(training_data, classify)
% PLOT_DECISION_REGION of classify with training_data superposed
    
    % Concatenate all training data
    d = cat(1, training_data{:});
    
    % Calculate min and max for x and y
    mins = min(d);
    maxs = max(d);
    xmin = mins(1) - 1;
    ymin = mins(2) - 1;
    xmax = maxs(1) + 1;
    ymax = maxs(2) + 1;
    
    % Set up dimension of decision region image
    % Increasing dim will give a smoother image result but will take
    % significantly longer to generate.
    dim = 200;
    xstep = (xmax - xmin) / dim;
    ystep = (ymax - ymin) / dim;
    
    % Initialize decision region image
    img = zeros(dim);
    
    % Classify each point in img
    for i=1:dim
        for j=1:dim
            x = [xmin + i * xstep; ymin + j * ystep];
            img(j, i) = classify(x);
        end
    end
    
    % Set up color map for class 1, 2 and 3
    cmap = [0.8510 0.3647 0.2549; ...
            0.5647 0.6235 0.8118; ...
            0.4000 1.0000 0.4000];
    
    % Set up plot map for training data
    pmap = [0.6 0 0; 0 0 0.6; 0 0.7 0];
    
    % Apply color map and display image
    colormap(cmap)
    image([xmin xmax], [ymin ymax], img);
    axis xy
    hold
    
    % Plot training data
    for i=1:size(training_data, 2)
        plot(training_data{i}(:,1), training_data{i}(:,2), ...
            '.', 'MarkerEdgeColor', pmap(i,:));
    end
    hold
    
end