import glob
import json

def parse(file):
    with open(file, 'r') as f:
        text = f.read() 
        section = text.split('>>')[2]
        lines = section.split('\n')
        result = {
            'name': lines[0]
        }

        scores_line = [s for s in lines[1].split(' ') if s != ""]
        if scores_line[0] == "rev-comp":
            result["rev-comp"] = True
            i = 1
        else:
            result["rev-comp"] = False
            i = 0

        attr = ""
        while i<len(scores_line):
            attr += scores_line[i]
            if attr[-1] == ':':
                result[attr[:-1]] = float(scores_line[i+1])
                attr = ""
                i += 2
            else:
                attr += " "
                i += 1

        similarities = [float(s[:-1].replace('(', '')) for s in lines[2].split(' ') if s[-1] == '%']
        result["identity%"] = similarities[0]
        result["similar%"] = similarities[1]

        indices = [int(x) for x in lines[2].split(' ')[-1][7:-1].split('-')]
        result["range"] = {
            "from": indices[0],
            "to": indices[1]
        }

        sequence = lines[7][lines[5].count(' ') + 6:]
        sequence += lines[13][7:] + lines[19][7:] + lines[25][7:]
        sequence += lines[31][7:-lines[29].count(' ')+1]

        result["sequence"] = sequence

        return result


for txt in glob.glob("outputs/*.output"):
    print("Parsing", txt)
    data = parse(txt)
    with open(txt.replace(".output", ".json"), "w+") as f:
        json.dump(data, f, indent=2)
