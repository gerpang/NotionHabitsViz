import json
import pandas as pd 

class ChartGenerator():
    
    def __init__(self):
        self.filepath = './data/habits.json'
        self.data = self.get_data()
        self.print_data_stats()
    
    def get_data(self):
        with open(self.filepath, 'r') as f:
            data_dict = json.load(f)    
        return pd.DataFrame.from_dict(data_dict,orient='index')

    def print_data_stats(self):
        data = self.data
        print("""There are {} entries, beginning {} and ending {}.
        """.format(len(data), min(data),max(data)))
        for col in self.data:
            print("""{}: {} out of {} ({}%)""".format(col, self.data[col].sum(), len(self.data), self.data[col].sum()/ len(self.data)*100 ))

if __name__ == "__main__":
    cg = ChartGenerator()