function [Line2D_Detected] = extract_lines(OUTPUT_img, IMG_SIZE)
%% Function created by Robert Frohlich

Line2D_Detected = [];
Lines_detected_count = 1;


numPixel_thr = 10;
inClusterAngleThr = 10;


T = adaptthresh(OUTPUT_img, 0.4);
Bin_OUTPUT = imbinarize(OUTPUT_img,T);

CC = bwconncomp(Bin_OUTPUT(:,:,1));  % use network image for clustering

numPixels = cellfun(@numel,CC.PixelIdxList);
keep = numPixels>=numPixel_thr*0.9; % clusters smaller than 48 pixel cannot contain a line long enough
CCfilt = CC.PixelIdxList(keep);

for cidx=1:length(CCfilt)
    
    temp = zeros(IMG_SIZE,IMG_SIZE);
    temp(CCfilt{cidx}) = 1;  % this will be the binary cluster image
    temp_gray = OUTPUT_img .* uint8(temp); % this is the corresponding gray image of the cluster
    
    lines = [];
    
    while sum(sum(temp)) >= numPixel_thr*0.9
        
        % hough -Matlab example code
        [H,theta,rho] = hough(temp_gray);
        
        P = houghpeaks(H,1,'threshold',ceil(0.3*max(H(:))));
        line1 = houghlines(temp_gray,theta,rho,P,'FillGap',numPixel_thr,'MinLength',numPixel_thr);
        if isempty(line1)
            break  % if no more lines can e extracted with hough, break
        end
        
        % check length of line
        len = norm(line1(1).point1 - line1(1).point2);
        if len >= numPixel_thr
            if isempty(lines) % if it's the firs line just add it
                lines = [lines; line1(1).point1,  line1(1).point2];
                
                Line2D_Detected(Lines_detected_count,:) = [line1(1).point1,  line1(1).point2];
                Lines_detected_count = Lines_detected_count + 1;
            else
                
                % check the angle if its different
                dir_vects = [(lines(:,1)-lines(:,3)).^2 , (lines(:,2)-lines(:,4)).^2 ];
                dir_vects(:,3) = 0;
                u = [ (line1(1).point1(1)-line1(1).point2(1))^2, (line1(1).point1(2)-line1(1).point2(2))^2, 0];
                VThetaInDegrees =atan2d( vecnorm(cross(dir_vects,repmat(u, [size(dir_vects,1),1]),2),2,2) , dot(dir_vects,repmat(u, [size(dir_vects,1),1]),2) );
                % https://www.mathworks.com/matlabcentral/answers/101590-how-can-i-determine-the-angle-between-two-vectors-in-matlab
                
                if sum(VThetaInDegrees <inClusterAngleThr) < 1
                    % if it's the same angle as a previous line from same
                    % cluster, than we don't add it
                    
                    % save the line as a good one
                    lines = [lines; line1(1).point1,  line1(1).point2];
                    
                    Line2D_Detected(Lines_detected_count,:) = [line1(1).point1,  line1(1).point2];
                    Lines_detected_count = Lines_detected_count + 1;
                    
                end
                
            end
        end
        
        % remove the detected line, even if it was short
        % both from binary and gray image
        line_img = insertShape(zeros(IMG_SIZE,IMG_SIZE), 'Line',[ line1(1).point1(1) line1(1).point1(2) line1(1).point2(1) line1(1).point2(2)],'LineWidth',4,'SmoothEdges', true, 'Color', [255 255 255] );
        %%% we have to modify here the parameters a little, because
        %%% otherwise it can get in an infinite loop easily with the real
        %%% output images
        
        temp = temp .* ~(logical (line_img(:,:,1)));
        temp_gray = OUTPUT_img .* uint8(temp);
        
        
    end
    
end



end


