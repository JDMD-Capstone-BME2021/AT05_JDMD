classdef Session < handle
    %SESSION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        Nsamples
        Angle
        Projections
        Preprocessed = []
        Reconstruction
        NChannels
        Imsize
    end
    
    methods
        function obj = Session()
            %SESSION Construct an instance of this class
            %   Detailed explanation goes here
        end
        
        function from_array(obj, I)
            %FROM_ARRAY loads images from array
            %Inputs:
            %   obj (Session):  instance of Session
            %   I(?x?x?x?):     4-dimensional image array with 3rd
            %   dimension indexing color channel and 4th dimension indexing
            %   images
            %   angle (1x1 double): total rotation angle
            obj.Projections = I;
        end
        
        function fbp(obj)
            if isempty(obj.Preprocessed)
                obj.Preprocessed = obj.Projections;
            end
            
            if obj.Angle <= 0
                error("Wrong angle value");
            end
            
            sz = size(obj.Preprocessed);
            obj.NChannels = sz(3);
            obj.Nsamples = sz(4);
            obj.Imsize = sz(1:2);
            
            wb = waitbar(0.0,'Please wait...');
            % calculate projection angles
            theta = linspace(0, obj.Angle, obj.Nsamples);
            % output size of reconstruction
            output_size = 2*floor(size(squeeze(obj.Preprocessed(1,:,:)),1)...
                /(2*sqrt(2))); % (from MATLAB docs)
            reconstruction = zeros([output_size output_size...
                obj.NChannels obj.Imsize(1)], class(obj.Preprocessed));
            n = obj.Imsize(1); % number of sinograms
            % reconstruct images
            for i = 1:obj.NChannels % color channel indexing
                for j = 1:n % sinogram indexing
                    msg = sprintf("Reconstructing channel %d out of %d",...
                        i, obj.NChannels);
                    waitbar(j/n, wb, msg);
                    reconstruction(:,:,i,j) =...
                        iradon(squeeze(obj.Preprocessed(j,:,i,:)), theta);
                end
            end
            obj.Reconstruction = reconstruction;
            delete(wb);
        end
        
        function I = get_slice(obj, n, axis)
            switch axis
                case 1
                    I = squeeze(obj.Reconstruction(n,:,:,:));
                    I = permute(I, [1,3,2]);
                case 2
                    I = squeeze(obj.Reconstruction(:,n,:,:));
                    I = permute(I, [1,3,2]);
                case 3
                    I = squeeze(obj.Reconstruction(:,:,:,n));
            end
            I = normalize(I, 'range');
        end
    end
end

