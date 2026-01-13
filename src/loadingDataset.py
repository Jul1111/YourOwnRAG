dataset = []

def load_dataset(filename):
    with open(filename,'r') as file:
        dataset = file.readlines()
        print(f'Loaded {len(dataset)} entries')
        return dataset