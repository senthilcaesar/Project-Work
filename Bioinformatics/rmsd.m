file1 = 'C:\Users\toshiba\Desktop\20set1_r.txt';
file2 = 'C:\Users\toshiba\Desktop\20set2.txt';
set1 = load(file1);
set2 = load(file2);
rmsd_normal = rms(set1,set2); % Normal rmsd
mean_set1 = mean(set1); % Centroid of set1
mean_set2 = mean(set2); % Centroid od set2
set1_new  = set1 - mean_set1; % New coordinates of the atom of set1
set2_new  = set2 - mean_set2; % New coordinates of the atom of set2
rmsd_optimized = rms(set1_new,set2_new); % Optimized rmsd

function [ rmsd ] = rms(set1,set2)
n_atoms = size(set1,1);
sd      = (set1-set2).^2;
total   = sum(sum(sd));
avg     = total/n_atoms;
rmsd    = sqrt(avg);
end
