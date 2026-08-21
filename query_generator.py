from PIL import Image
import numpy as np
import random
import json

START_FRAME = 0

random.seed(100)

def png_to_np_array(filename, HEIGHT, WIDTH):
    img = Image.open(filename).resize((WIDTH, HEIGHT))
    data = np.array(img.getdata()).reshape(img.size[1], img.size[0], 3)
    bindata = np.zeros((img.size[1], img.size[0]), np.uint32)
    for i, row in enumerate(data):
        for j, byte in enumerate(row):
            bindata[i, j] = 1 if sum(byte) > 127*3 else 0
    return bindata

def generate_queries_by_coordinate(HEIGHT, WIDTH, FRAMES, FPS):
    outputs = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            row.append("")
        outputs.append(row)

    for f in range(START_FRAME+1, START_FRAME+FRAMES+1, 24//FPS):
        bindata = png_to_np_array(f"frames/frame{f:04d}.png", HEIGHT, WIDTH)
        print(f"Processing frame {f}                         ", end='\r', flush=True)
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if bindata[i, j] == 1:
                    outputs[i][j] += random.choice(('C','T'))
                else:
                    outputs[i][j] += random.choice(('A','G'))

    for i in range(HEIGHT):
        for j in range(WIDTH):
            with open(f'queries/query_{i:02d}_{j:02d}.fa', "w+") as file:
                file.write(f">BA_{i}_{j}\n{outputs[i][j]}")

    with open(f'queries/meta.json', 'w+') as meta_file:
        json.dump({
            'height': HEIGHT,
            'width': WIDTH,
            'frames': FRAMES,
            'fps': FPS
        }, meta_file, indent=2)

    print("Done!                                                  ")

def generate_queries_by_frame(HEIGHT, WIDTH, FRAMES, FPS):
    for f in range(START_FRAME+1, START_FRAME+FRAMES+1, 24//FPS):
        bindata = png_to_np_array(f"frames/frame{f:04d}.png", HEIGHT, WIDTH)
        print(f"Processing frame {f}                         ", end='\r', flush=True)
        s = ""
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if bindata[i, j] == 1:
                    s += random.choice(('C','T'))
                else:
                    s += random.choice(('A','G'))
        with open(f'queries/query_{f:04d}.fa', "w+") as file:
            file.write(f">BA_{f}\n{s}")

    with open(f'queries/meta.json', 'w+') as meta_file:
        json.dump({
            'height': HEIGHT,
            'width': WIDTH,
            'frames': FRAMES,
            'fps': FPS
        }, meta_file, indent=2)

    print("Done!                                                  ")

def generate_queries_by_line(HEIGHT, WIDTH, FRAMES, FPS):
    line_cache = {}
    identity = 0
    for f in range(START_FRAME+1, START_FRAME+FRAMES+1, 24//FPS):
        bindata = png_to_np_array(f"frames/frame{f:04d}.png", HEIGHT, WIDTH)
        print(f"Processing frame {f}                         ", end='\r', flush=True)
        
        frame_lines = []
        for i in range(HEIGHT):
            line = ""
            for j in range(WIDTH):
                line += str(bindata[i, j])
            if line not in line_cache:
                line_cache[line] = identity
                query = ""
                for l in line:
                    if int(l) == 1:
                        query += random.choice(('G', 'T'))
                    else:
                        query += random.choice(('A', 'C'))
                with open(f'queries/query_{identity:04d}.fa', 'w+') as query_file:
                    query_file.write(f">BA_{identity}\n{query}")
                identity += 1
            frame_lines.append(line_cache[line])
            
        with open(f'queries/frame_{f:04d}.json', 'w+') as frame_file:
            json.dump({'lines': frame_lines}, frame_file, indent=2)

    with open(f'queries/meta.json', 'w+') as meta_file:
        json.dump({
            'height': HEIGHT,
            'width': WIDTH,
            'frames': FRAMES,
            'fps': FPS,
            'cache': line_cache
        }, meta_file, indent=2)

    print(f"Done with {len(line_cache)} unique lines!                                                  ")