# published: 2021-12,
# Authors: Hichem Abdellali, Robert Frohlich, Viktor Vilagos, Zoltan Kato, 
# using Python 3.7.9 and Matlab (R2020b)
# All rights reserved.

# Important!
# ------------------------------------------------------------------------
# Please cite our [1] publication whenever you use the implementation.

# This software package contains pre-trained L2D2 pipline which include 
# the the pre-trained detector/descriptor, the line extraction code and 
# the patch creation code as described in paper [1].

# [1]: Hichem Abdellali, Robert Frohlich, Viktor Vilagos, Zoltan Kato; 
# L2D2: Learnable Line Detector and Descriptor, IEEE 3DV 2021

import os
import cv2
import torch
import argparse
import numpy as np
from torch.autograd import Variable
import torchvision.transforms as transforms
from functions.Utils import cv2_scale, np_reshape
from RAL_net_cov import get_L2_conv

parser = argparse.ArgumentParser(description='L2D2 inference code')

# --------------------------------------------------------------------------------------------------------
# ----------------------------------------- INPUT PARAM --------------------------------------------------
# --------------------------------------------------------------------------------------------------------
parser.add_argument('--resume', default='./../IN_OUT_DATA/INPUT_NETWEIGHT/checkpoint_line_descriptor.th', type=str, metavar='PATH', help='path to latest checkpoint (default: none)')
parser.add_argument('--output_location', default='./../IN_OUT_DATA/DESCRIPTORS/', type=str, metavar='PATH', help='path of the output folder')
parser.add_argument('--patch_location', default='./../IN_OUT_DATA/EXTRACTED_PATCHES/', type=str, metavar='PATH', help='path of patches')


def get_descriptors(weights_path, Patches_location , Output_location):

    transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.492967568115862), (0.272086182765434))])

    # --------------------------------------------------------------------------------------------------------
    # ----------------------------------------- LOAD THE NETWORK WEIGHTS -------------------------------------
    # --------------------------------------------------------------------------------------------------------
    model = torch.load(weights_path).cuda()
    # set the model to evaluation mode
    model.eval()

    # read all folder names (image names) that contain patches
    # --------------------------------------------------------------------------------------------------------
    # ----------------------------------------- READ THE IMAGE FOLDERS ---------------------------------------
    # --------------------------------------------------------------------------------------------------------
    dirs = os.listdir(Patches_location)
    count=1
    for folder_name in dirs:

            # check if the output folder exist, if not create the output folder
            if not os.path.exists(Output_location + folder_name):
                os.makedirs(Output_location + folder_name)

            # list the image folders
            listPng = os.listdir(Patches_location + folder_name)

            # loop through the patches and provide the 128 descriptor that is saved in a text file
            # --------------------------------------------------------------------------------------------------------
            # ----------------------------------------- PROVIDE THE DESCRIPTOR ---------------------------------------
            # --------------------------------------------------------------------------------------------------------
            for i in range(0,len(listPng)):

                # patch path (directory/image name/ patch id .ext)
                PngName = Patches_location +'/'+ folder_name +'/'+ listPng[i][:-4] + '.png'

                # read the patch
                im = cv2.imread(PngName,0)
                img1_torch = transform(im)
                img1_torch = img1_torch.unsqueeze(0)
                img1_torch = Variable(img1_torch.float().cuda())
                y = model(img1_torch)

                # get the 128D descriptor array
                d1 = y.squeeze(0).detach().cpu().numpy()

                # write the descriptor in ta texte file such that each descriptor values are stored line by line
                np.savetxt(Output_location + folder_name +'/'+ listPng[i][:-4]+ ".txt", d1, fmt="%s")

            # print number of folders(images) / number of lines (patches) / folder name (image name)
            print(str(count) + ' ' + str(len(listPng)) + ' ' + str(folder_name))
            count= count + 1

#--------------------------------------------------------------------------------------------------------
#----------------------------------------- RUN INFERENCE ------------------------------------------------
#--------------------------------------------------------------------------------------------------------
def main():

    args = parser.parse_args()

    # --------------------------------------------------------------------------------------------------------
    # ------------------------------ SET THE INPUT/OUTPUT FOLDER + NET WEIGHT --------------------------------
    # --------------------------------------------------------------------------------------------------------
    NetWorkThLocation = args.resume
    Patches_location = args.patch_location
    Output_location = args.output_location

    if not os.path.exists(Output_location):
        os.mkdir(Output_location)

    get_descriptors(weights_path=NetWorkThLocation, Patches_location=Patches_location, Output_location=Output_location)

if __name__ == '__main__':
    main()