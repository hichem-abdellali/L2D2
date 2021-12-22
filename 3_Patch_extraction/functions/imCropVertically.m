function [imCroped] = imCropVertically(im,Line,boxWidth,boxHeight)
%IMCROPVERTICALLY : vertically rotate the detected line and extract the 
%centered patch from the top endpoint of the line


x1 = Line(1);
y1 = Line(2);
x2 = Line(3);
y2 = Line(4);

%# pick the top coordinate
if y2<y1
    tempx = x1;
    tempy = y1;
    x1 = x2;
    y1 = y2;
    x2 = tempx;
    y2 = tempy;            
end
    %# get the line angle to the vertical axe
    a = (y2-y1) / (x2 - x1);
    rad = atan(a);
    degree = rad * (180/pi);
    
    %imshow(im);

    % get the rotation matrix based on the rotation sign
    if degree >0

        [RotM,newY,newX] = getRotatedM(im, (degree)-90);
        %imrotatedTest = imrotate(im,(degree)-90,'nearest','loose');
        %[imrotatedTest] = rotateP2(im, (degree)-90);

    else
       [ RotM,newY,newX] = getRotatedM(im, 90 + (degree));
        %imrotatedTest = imrotate(im,90 + (degree),'nearest','loose');
        %[imrotatedTest] = rotateP2(im, 90 + (degree));

    end
        
    % 
    RotatedImage = zeros(round(newY), round(newX));
    PointLineTop = [y1,x1,1;y2,x2,1]';
    RotatedLineTop = round(rotatePM(PointLineTop, RotM));

    % coordinate of the bounding box
    BoxCoord = round(CropBoundingBox(RotatedImage, RotatedLineTop(2,1), RotatedLineTop(1,1), RotatedLineTop(2,2), RotatedLineTop(1,2), 16));

    % extract the 48x32 patch 
    [imCroped] = ExtractPixelBox3(BoxCoord(1,2), BoxCoord(1,1), boxWidth, boxHeight,RotatedImage,im,RotM);        

    end
    
