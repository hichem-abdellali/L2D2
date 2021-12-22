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
%%%%%%%%%%%%%%%%%%%%%%% INPUT PATH %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
IMG_SIZE = 512;
NETWORK_INPUT = ['./../IN_OUT_DATA/HEATMAPS_DIR/'];
NETWORK_OUTPUT = ['./../IN_OUT_DATA/EXTRACTED_LINES/'];
mkdir(NETWORK_OUTPUT);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Load all png images in the NETWORK_INPUT folder
unique_names = dir([NETWORK_INPUT,'*.png']);

for ff=1:length(unique_names)
    %ff
    name = unique_names(ff).name(1:end-4);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
    tStart = tic;    
    
    % read the input image
    OUTPUT_img = imread([NETWORK_INPUT,name,'.png']);
    
    % call the line extraction function
    [Line2D_Detected] = extract_lines(OUTPUT_img,IMG_SIZE);
    
    tEnd = toc(tStart);
    
    % filter out detected lines with a length <48
    % the lines have to be with a length bigger or equal a 48 pixels,
    % otherwise the patch extraction will encounter errors
    indx = vecnorm(Line2D_Detected(:,1:2)'-Line2D_Detected(:,3:4)')>=48;
    Line2D_Detected = Line2D_Detected(indx,:);
    
    %fprintf('%d minutes and %f seconds\n', floor(tEnd/60), rem(tEnd,60));    
    disp([num2str(size(Line2D_Detected,1)),' lines detected on image(' num2str(ff),') ',name, ' ; time: ',num2str(floor(tEnd/60)), ' minutes and ', num2str(rem(tEnd,60)),' seconds'])
    
    %%% Visualize the Lines; uncomment if you want to visualise
    % colorArray = repmat([255 255 255], size(Line2D_Detected,1),1);
    % in_img = insertShape(zeros(IMG_SIZE,IMG_SIZE), 'Line',[ Line2D_Detected(:,1) Line2D_Detected(:,2) Line2D_Detected(:,3) Line2D_Detected(:,4)],'LineWidth',1,'SmoothEdges', false, 'Color', colorArray );
    % figure, imshow(in_img);
            
    save([NETWORK_OUTPUT,name,'.mat'],'Line2D_Detected');        
    
end

