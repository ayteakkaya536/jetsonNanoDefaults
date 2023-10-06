## WORKS TESTED!!##
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
import torch
if torch.cuda.is_available():
    device = torch.device('cuda')
    print('yes CUDA available')
else:
    device = torch.device('cpu')
    print('no cuda is not available')

import time

matrix_size = 32*512 #firs number must be 32, which is batch size
x= torch.randn(matrix_size,matrix_size)
y= torch.randn(matrix_size,matrix_size)

print('*************CPU TIME ***********')
start=time.time()
result=torch.matmul(x,y)
print(time.time()-start)
print('verify device',result.device)

# GPU SETUP)
x_gpu=x.to(device)
y_gpu=y.to(device)
torch.cuda.synchronize()

for i in range(3): #first time of GPU cal takes longer, we eant to see normal speed
    print('*************GPU TIME ***********')
    start=time.time()
    result_gpu=torch.matmul(x_gpu,y_gpu)
    torch.cuda.synchronize()
    print(time.time()-start)
    print('verify device',result_gpu.device)
