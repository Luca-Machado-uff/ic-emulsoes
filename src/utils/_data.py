import os
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from torchvision import transforms
import cv2


class EmulsionDataset(Dataset):
    def __init__(self, file, root_dir, min_bubble_size=1, transform=None):
        if file.endswith(".xlsx"):
            self.sizes_frame = pd.read_excel(file)
        if file.endswith(".csv"):
            self.sizes_frame = pd.read_csv(file)
        self.root_dir = root_dir
        self.min_bubble_size = min_bubble_size
        self.transform = transform
        self.scale = (float(self.sizes_frame.iloc[:, 3].min()) * 5)/self.min_bubble_size

    def __len__(self):
        return len(self.sizes_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.sizes_frame.iloc[idx, 1])
        img = cv2.imread(img_name, 1)
        img = cv2.resize(img, (0, 0), fx=self.scale, fy=self.scale)
        meta_data = self.sizes_frame.iloc[idx, 2:5]
        sizes = self.sizes_frame.iloc[idx, 5:]
        sizes = np.asarray(sizes)
        meta_data = np.asarray(meta_data)
        if self.transform:
            img = self.transform(img)

        # return {'img': img, 'meta': meta_data, 'sizes': sizes}
        return img, meta_data.astype(np.float32), sizes.astype(np.float32)
