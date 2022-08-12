import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as f

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class WaterOnOilVGG16(nn.Module):
    def __init__(self, n_classes):
        super(WaterOnOilVGG16, self).__init__()
        # conv layers: (in_channel size, out_channels size, kernel_size, stride, padding)
        self.conv1_1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.conv1_2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)

        self.conv2_1 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv2_2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)

        self.conv3_1 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.conv3_2 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.conv3_3 = nn.Conv2d(256, 256, kernel_size=3, padding=1)

        self.conv4_1 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.conv4_2 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.conv4_3 = nn.Conv2d(512, 512, kernel_size=3, padding=1)

        self.conv5_1 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.conv5_2 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.conv5_3 = nn.Conv2d(512, 512, kernel_size=3, padding=1)

        # max pooling (kernel_size, stride)
        self.pool = nn.MaxPool2d(2, 2)

        # fully conected layers:
        self.fc6 = nn.Linear(7*7*512, 4096)
        self.fc7 = nn.Linear(4096, 4096)
        self.fc8 = nn.Linear(4096, 1000)

    def forward(self, x, training=True):
        x = f.relu(self.conv1_1(x))
        x = f.relu(self.conv1_2(x))
        x = self.pool(x)
        x = f.relu(self.conv2_1(x))
        x = f.relu(self.conv2_2(x))
        x = self.pool(x)
        x = f.relu(self.conv3_1(x))
        x = f.relu(self.conv3_2(x))
        x = f.relu(self.conv3_3(x))
        x = self.pool(x)
        x = f.relu(self.conv4_1(x))
        x = f.relu(self.conv4_2(x))
        x = f.relu(self.conv4_3(x))
        x = self.pool(x)
        x = f.relu(self.conv5_1(x))
        x = f.relu(self.conv5_2(x))
        x = f.relu(self.conv5_3(x))
        x = self.pool(x)
        x = x.view(-1, 7 * 7 * 512)
        x = f.relu(self.fc6(x))
        x = f.dropout(x, 0.5, training=training)
        x = f.relu(self.fc7(x))
        x = f.dropout(x, 0.5, training=training)
        x = self.fc8(x)
        return x

    def predict(self, x):
        x = f.softmax(self.forward(x, training=False))
        return x

        prediction = self.predict(x)
        maxs, indices = torch.max(prediction, 1)
        acc = 100 * torch.sum(torch.eq(indices.float(), y.float()).float())/y.size()[0]
        return acc.cpu().data[0]
