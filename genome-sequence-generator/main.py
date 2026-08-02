from PIL import Image
import numpy as np
import random

START_FRAME = 0
FRAMES = 5257
FPS = 24

HEIGHT = 20
WIDTH = 20

def png_to_np_array(filename):
    # print(WIDTH, HEIGHT)
    img = Image.open(filename).resize((WIDTH, HEIGHT))
    # print(img.size)
    data = np.array(img.getdata()).reshape(img.size[1], img.size[0], 3)
    bindata = np.zeros((img.size[1], img.size[0]), np.uint32)
    for i, row in enumerate(data):
        for j, byte in enumerate(row):
            bindata[i, j] = 1 if sum(byte) > 127*3 else 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            print('#' if bindata[i, j] == 1 else ' ', end='')
        print()
    return bindata

outputs = []
for i in range(HEIGHT):
    row = []
    for j in range(WIDTH):
        row.append("")
    outputs.append(row)

for f in range(START_FRAME+1, START_FRAME+FRAMES+1, 24//FPS):
    bindata = png_to_np_array(f"frames/frame{f}.png")
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if bindata[i, j] == 1:
                outputs[i][j] += random.choice(('C','T'))
            else:
                outputs[i][j] += random.choice(('A','G'))

for i in range(HEIGHT):
    for j in range(WIDTH):
        with open(f'outputs/query_{i}_{j}.fa', "w+") as file:
            file.write(f">BA_{i}_{j}\n{outputs[i][j]}")