import torch
import torch.nn as nn


class simam_module(torch.nn.Module):
    def __init__(self, channels=None, e_lambda=1e-4):
        super(simam_module, self).__init__()

        self.activaton = nn.Sigmoid()
        self.e_lambda = e_lambda

    def __repr__(self):
        s = self.__class__.__name__ + '('
        s += ('lambda=%f)' % self.e_lambda)
        return s

    @staticmethod
    def get_module_name():
        return "simam"

    def forward(self, x):
        b, c, h, w = x.size()

        n = w * h - 1

        x_minus_mu_square = (x - x.mean(dim=[2, 3], keepdim=True)).pow(2)
        v = x_minus_mu_square.sum(dim=[2, 3], keepdim=True) / n
        y = x_minus_mu_square / (4 * v + self.e_lambda) + 0.5
        # y_max = torch.max(y)      # debug
        # print(y_max)
        att = self.activaton(y)

        return x * att


if __name__ == '__main__':
    x = torch.randn(1, 3, 256, 256)
    simam = simam_module(3)
    a = simam(x)
