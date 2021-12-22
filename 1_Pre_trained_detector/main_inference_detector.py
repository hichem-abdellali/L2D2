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
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
from functions import dataLoader
from functions.detector_network_L2D2 import line_detection_network
import matplotlib.pyplot as plt

os.environ['CUDA_VISIBLE_DEVICES'] = "0"

#--------------------------------------------------------------------------------------------------------
#----------------------------------------- INPUT PARAM --------------------------------------------------
#--------------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='L2D2 inference code')

parser.add_argument('--resume', default='./../IN_OUT_DATA/INPUT_NETWEIGHT/checkpoint_line_detector.pth.tar', type=str, metavar='PATH', help='path to latest checkpoint')
parser.add_argument('--input_location', default='./../IN_OUT_DATA/INPUT_IMAGES/', type=str, metavar='PATH', help='path of the input folder')
parser.add_argument('--output_location', default='./../IN_OUT_DATA/HEATMAPS_DIR/', type=str, metavar='PATH', help='path of the output folder')

#--------------------------------------------------------------------------------------------------------
#----------------------------------------- RUN INFERENCE ------------------------------------------------
#--------------------------------------------------------------------------------------------------------
def inference_call(val_loader, model,PathSave):
    with torch.no_grad():
        for i, (input1, image_name) in enumerate(val_loader):
            line_detected = model.forward(input1)

            # Normalized the heatmap between ]0 and 1]
            ii = np.transpose(line_detected[0, :, :, :].cpu().detach().numpy(), axes=[1, 2, 0])
            normalized = (ii - np.min(ii)) / (np.max(ii) - np.min(ii)+1e-16)

            # save the heatmap as a png
            cv2.imwrite(PathSave + str(image_name[0]) + '.png', normalized * 255)

            # DEBUG: display the heatmap, don't forget to make sure that plt is imported
            # plt.imshow(normalized_line[0,0,:,:].cpu().detach().numpy(), cmap='gray')

            # print image names
            print('Image '+str(i+1) + ': ' + image_name[0] + ' processed')


def main():

    global args
    args = parser.parse_args()

    # --------------------------------------------------------------------------------------------------------
    # ----------------------------------------- LOAD THE DATA ------------------------------------------------
    # --------------------------------------------------------------------------------------------------------

    normalize = transforms.Normalize(mean=[0.492967568115862], std=[0.272086182765434])
    transform_train = transforms.Compose([ transforms.ToTensor(), normalize, ])
    train_loader = torch.utils.data.DataLoader(dataLoader.Loader(args.input_location,transform=transform_train),batch_size=1, num_workers=4)

    # --------------------------------------------------------------------------------------------------------
    # ----------------------------------------- LOAD THE NETWORK ---------------------------------------------
    # --------------------------------------------------------------------------------------------------------
    model = line_detection_network()
    model = model.to('cuda')
    model = torch.nn.DataParallel(model).cuda()

    # --------------------------------------------------------------------------------------------------------
    # ----------------------------------------- LOAD THE WEIGHTS ---------------------------------------------
    # --------------------------------------------------------------------------------------------------------
    if args.resume:
        if os.path.isfile(args.resume):
            print("=> loading checkpoint '{}'".format(args.resume))
            checkpoint = torch.load(args.resume)
            model.load_state_dict(checkpoint['state_dict'])
            print("=> loaded checkpoint '{}' (epoch {})"
                  .format(args.resume, checkpoint['epoch']))
        else:
            print("=> no checkpoint found at '{}'".format(args.resume))
            return
    # --------------------------------------------------------------------------------------------------------
    # ----------------------------------------- CREATE THE OUTPUT FOLDER -------------------------------------
    # --------------------------------------------------------------------------------------------------------
    if not os.path.exists(args.output_location):
        os.makedirs(args.output_location)
    # --------------------------------------------------------------------------------------------------------
    # ----------------------------------------- CALL THE INFERENCE FUNCTION ----------------------------------
    # --------------------------------------------------------------------------------------------------------
    model.eval()
    inference_call(train_loader, model,args.output_location)
    print ('Line detection code executed with success')


if __name__ == '__main__':
    main()
