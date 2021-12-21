# L2D2: Learnable Line Detector and Descriptor

This repository contains the pre-trained network implementation of the following [paper](https://www.researchgate.net/publication/355340221_L2D2_Learnable_Line_Detector_and_Descriptor):

it includes the the pre-trained detector/descriptor, the line extraction matlab code and the patch creation matlab code

```text
@inproceedings{l2d2,
  author    = {Hichem Abdellali, Robert Frohlich, Viktor Vilagos, Zoltan Kato},
  title     = {{L2D2:} Learnable Line Detector and Descriptor},
  booktitle = {IEEE International Conference on 3D Vision (3DV)},
  year      = {2021},
}
```

Getting started
-----------------
You just need a conda envirement with Python 3.8+
```
conda env create -f l2d2.yml python=3.8
```
for the Matlab code, it does not require any installation, the Package contains all the necessary functions. 
The code needs input images of 512x512 pixels (an example is provided inside `IN_OUT_DATA/INPUT_IMAGES/)



Pretrained models Getting started
-----------------
We provided the pre-trained models in the `IN_OUT_DATA/INPUT_NETWEIGHT/` folder:
 - `checkpoint_line_detector.pth.tar`: this is the pre-trained model for the line detector.
 - `checkpoint_line_descriptor.th`: this is the pre-trained model for the line descriptor.



Please cite publication whenever you use the implementation:  
*H.Abdellali*, *R.Frohlich*, *V.Vilagos*, *Z.Kato*, *Learnable Line Detector and Descriptor*, *IEEE International Conference on 3D Vision (3DV)*, *2021*
