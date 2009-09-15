% Load the dataset
load Datasets/ls_group14.txt
dataset = ls_group14;

%plot(dataset(:,1), dataset(:,2), '.r')

% Split data into 3 classes
c1 = dataset(1:500,:);
c2 = dataset(501:1000,:);
c3 = dataset(1001:end,:);

%plot(c1(:,1), c1(:,2), '.r', c2(:,1), c2(:,2), '.g' , c3(:,1), c3(:,2), '.b')

% Use 75% of data for training
t1 = c1(1:375,:);
t2 = c2(1:375,:);
t3 = c3(1:375,:);

% Use 25% of data for testing
test_data = [c1(376:end,:); c2(376:end,:); c3(376:end,:)];




