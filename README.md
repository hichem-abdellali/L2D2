# L2D2: Learnable Line Detector and Descriptor

This repository contains the pre-trained network implementation of the following [paper](https://www.researchgate.net/publication/355340221_L2D2_Learnable_Line_Detector_and_Descriptor):

Please cite this publication whenever you use the implementation:  
```text
@inproceedings{l2d2,
  author    = {Hichem Abdellali, Robert Frohlich, Viktor Vilagos, Zoltan Kato},
  title     = {{L2D2:} Learnable Line Detector and Descriptor},
  booktitle = {IEEE International Conference on 3D Vision (3DV)},
  address      = {{United kingdom, London} (online)},  
  year      = {2021},
}
```

The repository contains the full L2D2 pipeline which includes: the pre-trained detector/descriptor python code, the line extraction matlab code and the patch creation matlab code.

For the Matlab code, the Package contains all the necessary functions.

Getting started
-----------------
You just need a conda environment with Python 3.7.9

```
conda env create -f l2d2.yml
```

The full L2D2 pipeline needs input images of *512x512* pixels (an example is provided inside `IN_OUT_DATA/INPUT_IMAGES/`)

To obtain the detected lines and the descriptors, run the 4 programs which compose the full L2D2 pipeline in the following orders 
```
(l2d2) > python main_inference_detector.py
>> line_extraction_heatmap.m  (matlab code)
>> main_Patch_creation.m (matlab code)
(l2d2) > python main_Inference_descriptor.py
```

1. `main_inference_detector.py` located inside `1_Pre_trained_detector`: loads the images from the folder `INPUT_IMAGES` and provides a heatmap of *512x512* for each input image in HEATMAPS_DIR
2. `line_extraction_heatmap.m` located inside `2_Line_extraction`: loads the heatmaps from `HEATMAPS_DIR` and provides the detected lines in a `.mat` file in the EXTRACTED_LINES folder
3. `main_Patch_creation.m` located inside `3_Patch_extraction`: reads the lines from the folder `EXTRACTED_LINES` of each image and provides a patch of *48x32* for each 2D line, the patches are stored in the `EXTRACTED_PATCHES` folder
4. `main_Inference_descriptor.py` located inside `4_Pre_trained_descriptor`: loads the patches from the folder `EXTRACTED_PATCHES and provides the descriptor in folder `DESCRIPTORS`

All the input/output data is located inside the folder `IN_OUT_DATA`

Pretrained models
-----------------
We provided the pre-trained models in the `IN_OUT_DATA/INPUT_NETWEIGHT/` folder:
 - `checkpoint_line_detector.pth.tar`: this is the pre-trained model for the line detector.
 - `checkpoint_line_descriptor.th`: this is the pre-trained model for the line descriptor.


NOTE: the detector/descriptor training code and the training data generation code will be released later
