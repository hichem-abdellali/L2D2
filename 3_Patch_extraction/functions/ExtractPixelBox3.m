function [ListU] = ExtractPixelBox3(i1, j1,w,l,RotatedImage,im,RotMatfull)

    %im=rgb2gray(im);
    [oldY,oldX,~] = size(im);
    [newY,newX,~] = size(RotatedImage);
    
    list = zeros(round(l), round(w));
    
    point = zeros(l*w,3);
    start = floor([i1,j1]);
    count=1;
    for i=1:l
        for j=1:w
            point(count,:) = [i+start(1)-1, j+start(2)-1, 1];     
            count = count+ 1;
        end
    end    
    
    %pointRo = floor(inv(RotMatfull) * point');
    pointRo = floor(RotMatfull \ point');
    
    count = 1;
    for i=1:l
        for j=1:w
            point = [i+start(1)-1, j+start(2)-1, 1];
            pointR =  pointRo(:,count);
            if (pointR(1))>=1 && (pointR(1))<= oldY &&  (pointR(2))>=1 && (pointR(2))<=oldX && (point(1))>=1 && (point(1))<= newY &&  (point(2))>=1 && (point(2))<=newX
                list(i,j) = im(pointR(1),pointR(2));
            else
                list(i,j) = 0;
            end
            count = count + 1;
        end
    end
    
    ListU = uint8(list);
    
  
end

