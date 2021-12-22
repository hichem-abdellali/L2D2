function [Nimgl] = CropBoundingBox(im,x1,y1,x2,y2,l)


    if y2 < y1
        tempx = x1;
        tempy = y1;
        x1 = x2;
        y1 = y2;
        x2 = tempx;
        y2 = tempy;
    end

    l = (l);
    %l2 = (l/2);
    l2 = 0;
    
    x1 = (x1);
    x2 = (x2);
    y1 = (y1);
    y2 = (y2);

    p1 = [x1-l,y1-l2,1];
    p2 = [x2+l,y2-l2,1];
    p3 = [x1+l,y2+l,1];
    p4 = [x2-l,y1+l,1];

    lengY = p4(2) - p1(2);
    lengX = p2(1) - p1(1);

    Nimgl = [p1;p2;p3;p4];

end

