import os
import pandas as pd
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

    def __len__(self):
        return len(self.sizes_frame)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.sizes_frame.iloc[idx, 1])
        img = cv2.imread(img_name, 1)
        grid_size = float(self.sizes_frame.iloc[idx, 3]) * 5
        scale = grid_size/self.min_bubble_size
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
        convert_tensor = transforms.ToTensor()
        convert_tensor(img)
        meta_data = self.sizes_frame.iloc[idx, 2:5]
        sizes = self.sizes_frame.iloc[idx, 5:]
        sample = {'img': img, 'meta': meta_data, 'sizes': sizes}
        if self.transform:
            sample = self.transform(sample)

        return sample
