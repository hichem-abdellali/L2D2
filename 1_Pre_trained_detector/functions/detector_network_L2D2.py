
import torch.nn as nn
import matplotlib.pyplot as plt

class Bottleneck2D(nn.Module):
    expansion = 2

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(Bottleneck2D, self).__init__()

        self.bn1 = nn.BatchNorm2d(inplanes)
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1)
        self.bn3 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 2, kernel_size=1)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.bn1(x)
        out = self.relu(out)
        out = self.conv1(out)

        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv2(out)

        out = self.bn3(out)
        out = self.relu(out)
        out = self.conv3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual

        return out

#Pool = nn.MaxPool2d

class Conv(nn.Module):
    def __init__(self, inp_dim, out_dim, kernel_size=3, stride = 1, bn = False, relu = True):
        super(Conv, self).__init__()
        self.inp_dim = inp_dim
        self.conv = nn.Conv2d(inp_dim, out_dim, kernel_size, stride, padding=(kernel_size-1)//2, bias=True)
        self.relu = None
        self.bn = None
        if relu:
            self.relu = nn.ReLU()
        if bn:
            self.bn = nn.BatchNorm2d(out_dim)

    def forward(self, x):
        #assert x.size()[1] == self.inp_dim, "{} {}".format(x.size()[1], self.inp_dim)
        x = self.conv(x)
        if self.bn is not None:
            x = self.bn(x)
        if self.relu is not None:
            x = self.relu(x)
        return x

class Net(nn.Module):

    def __init__(self, block):
        super(Net, self).__init__()
        #################################### Pre-activation part ###############################################

        self.inplanes = 64
        self.num_feats = 128
        self.ht_channels=16
        #self.batches= batches_size
        self.conv1 = nn.Conv2d(1, self.inplanes, kernel_size=7, stride=2, padding=3)
        self.relu = nn.ReLU(inplace=True)
        self.layer1 = self._make_residual(block, self.inplanes, 1)
        self.layer2 = self._make_residual(block, self.inplanes, 1)
        self.layer3 = self._make_residual(block, self.num_feats, 1)
        self.maxpool = nn.MaxPool2d(2, stride=2)

        self.deconv1 = nn.ConvTranspose2d(in_channels = 256, out_channels = 128, kernel_size = 4, stride = 2, padding = 1)
        self.bn1 = nn.BatchNorm2d(128)
        self.relu1 = nn.ReLU()
        self.deconv2 = nn.ConvTranspose2d(in_channels = 128, out_channels = 1, kernel_size = 4, stride = 2, padding = 1)
        self.bn2 = nn.BatchNorm2d(1)
        self.relu2 = nn.ReLU()
        self.conv = Conv(1, 1, 1, bn=False, relu=False)



    def _make_residual(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(
                    self.inplanes,
                    planes * block.expansion,
                    kernel_size=1,
                    stride=stride,
                )
            )

        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)


    def forward(self, x):

        ########################
        # Pre-activation part
        prea = self.conv1(x)
        prea = self.layer1(prea)
        prea = self.maxpool(prea)
        prea = self.layer2(prea)
        prea = self.layer3(prea)

        ########################
        line_dec1 = self.deconv1(prea)
        line_dec1 = self.bn1(line_dec1)
        line_dec1 = self.relu1(line_dec1)

        line_dec2 = self.deconv2(line_dec1)
        line_dec2 = self.bn2(line_dec2)
        line_dec2 = self.relu2(line_dec2)

        line_detected = self.conv(line_dec2)

        return line_detected
        # plt.imshow(line_HT_detected[0,0,:,:].cpu().detach().numpy(), cmap='gray')

def line_detection_network(**kwargs):
    model = Net(Bottleneck2D)
    return model
