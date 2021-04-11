function [FBdown,x,y,z] = render_vol(I, factorDown, noiseThreshold)
arguments
    I
    factorDown = 2
    noiseThreshold = 1.8
end
FB = double(I*255.0);
[nFy,~,nFz]=size(FB);
FBt =FB(:,:,:);
ny=round(nFy/factorDown); nx=round(nFy/factorDown); nz=round(nFz/factorDown); %% desired output dimensions

[y, x, z]=ndgrid(linspace(1,size(FBt,1),ny),linspace(1,size(FBt,2),nx),linspace(1,size(FBt,3),nz));
FBdown=interp3(FBt,x,y,z);
FBdown(FBdown<noiseThreshold)=0;
FBdown=FBdown(:,:,nz:-1:1);
FBdown = FBdown./max(FBdown(:))*255;
end

