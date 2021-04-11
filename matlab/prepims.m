function out = prepims(I, scale, grayscale)
%PREPIMS preprocesses an array of images
%Function takes a 4D array of grayscale or RGB images, scales it by the
%specified factor and converts if to grayscale if the flag is set
%Inputs:
%   I (?x?x?x?): array of images with 3rd dimension indexing channel and
%   4th dimension indexing images
%   scale (1x1 double): image scale factor
%   grayscale (1x1 logical): grayscale conversion flag
%Outputs:
%   out (?x?x?x?): array of images with 3rd dimension indexing color 
%   channel and 4th dimension indexing images
arguments
    I (:,:,:,:)
    scale (1,1) double
    grayscale (1,1) logical = false
end
wb = waitbar(0,'Please wait...');
n = size(I,4);
im = prepimg(squeeze(I(:,:,:,1)), scale, grayscale);
sz = size(im);
if grayscale
    sz = [sz 1 n];
else
    sz = [sz n];
end
assert(length(sz)==4); % assert output is 4D
out = zeros(sz, class(im));
out(:,:,:,1) = im;
waitbar(1/n, wb, 'Preprocessing images...');
for i = 2:n
    out(:,:,:,i) = prepimg(squeeze(I(:,:,:,i)), scale, grayscale);
    waitbar(i/n, wb, 'Preprocessing images...');
end
delete(wb);
end

function I = prepimg(I, scale, grayscale)
%PREPIMG preprocesses a single image
%Function takes a grayscale or RGB images, scales it by the specified 
%factor and converts if to grayscale if the flag is set
%Inputs:
%   I (?x?x?): array of images with 3rd dimension indexing channel
%   scale (1x1 double): image scale factor
%   grayscale (1x1 logical): grayscale conversion flag
%Outputs:
%   out (?x?x?): image with 3rd dimension indexing color channel
arguments
    I
    scale (1,1) double
    grayscale (1,1) logical
end
I = im2double(I);
if grayscale
    I = rgb2gray(I);
end
I = imcomplement(I);
I = imresize(I, scale);
I = normalize(double(I), 'range');
end