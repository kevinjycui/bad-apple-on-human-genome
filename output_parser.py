def parse(file):
    with open(file, 'r') as f:
        text = f.read() 
        section = text.split('>>')[2]
        lines = section.split('\n')
        result = {
            'Name': lines[0]
        }
        print(lines[1])


parse("outputs/fasta_0_0.output")