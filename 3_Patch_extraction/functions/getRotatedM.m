function [RotMatfull,newY,newX] = getRotatedM(im, a1)

    a = a1 * pi / 180;
    [oldY, oldX,~] = size(im);

    holdY = (oldY/ 2);
    holdX = (oldX/ 2);

    Tocenter = [1, 0, -holdY;0, 1, -holdX;0, 0, 1];

    Matrix = [cos(a),-sin(a), 0;sin(a), cos(a), 0; 0 ,0, 1];
    RotMat =  Matrix * Tocenter;

    [newS] = [abs(sin(a)*oldY) + abs(cos(a)*oldX),abs(sin(a)*oldX) + abs(cos(a)*oldY)];
    newX = newS(1);
    newY =  newS(2);
    cX = (newX/ 2);
    cY = (newY/ 2);

    Fromcenter = [1, 0, cY;0, 1, cX;0, 0, 1];
    RotMatfull = Fromcenter*RotMat;

    newX = round(newX);
    newY =  round(newY);    

end

