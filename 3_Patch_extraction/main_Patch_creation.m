% published: 2021-12,
% Authors: Hichem Abdellali, Robert Frohlich, Viktor Vilagos, Zoltan Kato, 
% using Python 3.7.9 and Matlab (R2020b)
% All rights reserved.

% Important!
% ------------------------------------------------------------------------
% Please cite our [1] publication whenever you use the implementation.

% This software package contains pre-trained L2D2 pipline which include 
% the the pre-trained detector/descriptor, the line extraction code and 
% the patch creation code as described in paper [1].

% [1]: Hichem Abdellali, Robert Frohlich, Viktor Vilagos, Zoltan Kato; 
% L2D2: Learnable Line Detector and Descriptor, IEEE 3DV 2021

restoredefaultpath
addpath './functions'


%%%%%%%%%%%%%%%%%%%%%%% INPUT PATH %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

INPUT_IMAGES_PATH =  ['./../IN_OUT_DATA/INPUT_IMAGES/'];
INPUT_IMAGE_LINE_PATH = ['./../IN_OUT_DATA/EXTRACTED_LINES/'];
DATA_OUT_PATH = ['./../IN_OUT_DATA/EXTRACTED_PATCHES/'];
Matfiles= dir([DATA_OUT_PATH]);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


unique_names = dir([INPUT_IMAGE_LINE_PATH,'*.mat']);

for ff=1:length(unique_names)
        
        %% Reading Lines and corresponding image        
        image_name = unique_names(ff).name(1:end-4) ;
        lines_data = load([INPUT_IMAGE_LINE_PATH,unique_names(ff).name],'Line2D_Detected');
        Line2D_Detected = lines_data.Line2D_Detected;        
        full_image = imread([INPUT_IMAGES_PATH,image_name,'.png']);
        
        %% create a folder for the patches
        mkdir([DATA_OUT_PATH,'/',image_name,'/'])
                
        %% create a patch for each detected 2D line
        for i=1:size(Line2D_Detected,1)
            [patch_cropped]= imCropVertically(full_image,Line2D_Detected(i,:),32, 48);
            imwrite(uint8(patch_cropped),[DATA_OUT_PATH,'/',image_name,'/',num2str(i),'.png']);
        end
        
end
