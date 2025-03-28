"""
Haar Wavelet-based Downsampling (HWD)
Original address of the paper: https://www.sciencedirect.com/science/article/abs/pii/S0031320323005174
Code reference: https://github.com/apple1986/HWD/tree/main
"""
import torch
import torch.nn as nn
from pytorch_wavelets import DWTForward
 
class HWDownsampling(nn.Module):
    def __init__(self, in_channel, out_channel):
        super(HWDownsampling, self).__init__()
        self.wt = DWTForward(J=1, wave='haar', mode='zero').to(torch.float16)
        self.conv_bn_relu = nn.Sequential(
            nn.Conv2d(in_channel * 4, out_channel, kernel_size=1, stride=1),
            nn.BatchNorm2d(out_channel),
            nn.ReLU(inplace=True),
        )
 
    def forward(self, x):
        yL, yH = self.wt(x)
        y_HL = yH[0][:, :, 0, ::]
        y_LH = yH[0][:, :, 1, ::]
        y_HH = yH[0][:, :, 2, ::]
        x = torch.cat([yL, y_HL, y_LH, y_HH], dim=1)
        x = self.conv_bn_relu(x)
        return x
 
 
if __name__ == '__main__':
    downsampling_layer1 = HWDownsampling(32, 64)
    downsampling_layer2 = HWDownsampling(64,128)
    input_data = torch.rand((2, 32, 256, 512))
    output_data = downsampling_layer1(input_data)
    final_out_data=downsampling_layer2(output_data)
    print("Input shape:", input_data.shape)
    print("Output shape:", output_data.shape)
    print("final_out_data: ",final_out_data.shape)