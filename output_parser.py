import glob
import json

def parse(file):
    with open(file, 'r') as f:
        text = f.read() 

        if len(text.split('>>')) <= 2:
            return {
                "status": "No sequence found"
            }
        
        section = text.split('>>')[2]
        lines = section.split('\n')

        result = {
            "status": "Sequence found",
            "name": lines[0]
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

        similarities = [float(s[:-1].replace('(', '')) for s in lines[2].split(' ') if s != "" and s[-1] == '%']
        result["identity%"] = similarities[0]
        result["similar%"] = similarities[1]

        indices = [x for x in lines[2].split(' ')[-1][7:-1].split('-')]
        result["range"] = {
            "from": indices[0],
            "to": indices[1]
        }

        query_i = 11
        sequence_i = 13
        space_offset = 6-len(lines[query_i].split(' ')[0])
        sequence = lines[7][lines[5].count(' ') + 6 - space_offset:]

        while lines[query_i].count(' ') == 1 + space_offset:
            sequence += lines[sequence_i][7:]
            query_i += 6
            sequence_i += 6
        sequence += lines[sequence_i][7:-lines[query_i].count(' ') + 1 + space_offset]

        result["sequence"] = sequence

        return result

def parse_to_json_files():
    sequences_found = 0
    sequences_not_found = 0

    for txt in glob.glob("outputs/*.output"):
        print("Parsing", txt)
        data = parse(txt)

        if data["status"] == "Sequence found":
            sequences_found += 1
        else:
            sequences_not_found += 1

        with open(txt.replace(".output", ".json"), "w+") as f:
            json.dump(data, f, indent=2)

    print("Sequences found:", sequences_found)
    print("Sequences not found:", sequences_not_found)
