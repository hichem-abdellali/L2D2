from PIL import Image, ImageOps
import os
import os.path
import PIL


class Loader():

    def __init__(self, root, transform=None):

        self.Input_images,self.Input_len = self.LoadPairs_corrected_test(root)
        self.transform = transform
        self.root = root

    def LoadPairs_corrected_test(self,root):
        InputImage = []
        batches = sorted(os.listdir(root))
        bacthes_size = len(batches)

        for b in range(0, bacthes_size):
            batchName = batches[b]
            InputImage.append(batchName)
        return InputImage,len(InputImage)


    def __len__(self):
        return len(self.Input_images)

    def __getitem__(self, index):

        img_1_p = self.root + self.Input_images[index]
        img1 = PIL.Image.open(img_1_p)
        img1 = ImageOps.grayscale(img1)
        img1_out = self.transform(img1)
        return img1_out,self.Input_images[index][:-4]



