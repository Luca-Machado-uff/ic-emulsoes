import os

from torch import optim, utils
from torch.utils.data import random_split
from ._model import WaterOnOilVGG16
from torchvision import transforms
from src.utils._data import EmulsionDataset
from src.utils._loss import EDMLoss


def water_on_oil():
    base_path = os.path.abspath(os.path.join(__file__, '../../../',
                                             'Filtered water on oil'))
    batch_size = 2
    transform = transforms.Compose([transforms.ToTensor()])
    dataset = EmulsionDataset((base_path + "/" + "óleo_em_água.xlsx"), base_path, transform=transform)

    dataset_train, dataset_test = random_split(dataset, [9, 2])

    train_loader = utils.data.DataLoader(dataset_train, batch_size=batch_size, shuffle=False)
    test_loader = utils.data.DataLoader(dataset_test, batch_size=batch_size, shuffle=False)

    network = WaterOnOilVGG16(41)

    criterion = EDMLoss()
    optimizer = optim.SGD(network.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(10):

        for i, data in enumerate(train_loader, 0):
            img, metadata, labels = data
            optimizer.zero_grad()
            outputs = network(img)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
