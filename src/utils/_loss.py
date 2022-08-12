from torch import cumsum, nn


class EDMLoss(nn.Module):
    def __init__(self):
        super(EDMLoss, self).__init__()

    def forward(self, input_, target):
        edm = input_ - target
        edm = cumsum(edm, dim=0)
        edm = edm.abs()
        return edm.sum()
