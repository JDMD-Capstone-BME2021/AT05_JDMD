function out = load_images(fpaths)
%LOAD_IMAGES Loads images into an matrix
%Inputs:
%   fpaths (cell ?x1): cell array containing image paths
%Outputs:
%   out: array containing images with 3rd dimension indexing color channels
%   and 4th dimension indexing images
wb = waitbar(0,'Please wait...');
n = length(fpaths); % get number of files
% read first image to get resolution & number of channels
im = imread(fpaths{1});
sz = size(im);
% if image is grayscale, we explicitly state it has 1 channel
if length(sz) == 2
    sz = [sz 1];
end
out = zeros([sz n], class(im)); % preallocate
out(:,:,:,1) = im;
waitbar(1/n, wb, 'Loading images...')
% read the rest of the images
for i = 2:n
    waitbar(i/n, wb, 'Loading images...')
    out(:,:,:,i) = imread(fpaths{i});
end
delete(wb);
end

