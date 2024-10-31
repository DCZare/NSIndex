# parse_GEN.py

import pandas as pd
from tkinter import Tk, filedialog

def split_name(full_name):
    name_parts = full_name.split()
    if len(name_parts) == 0:
        return [None, None, None]
    elif len(name_parts) == 1:
        return [name_parts[0], None, None]
    elif len(name_parts) == 2:
        return [name_parts[0], None, name_parts[1]]
    else:
        return [name_parts[0], " ".join(name_parts[1:-1]), name_parts[-1]]

def main():
    root = Tk()
    root.withdraw()
    file1_path = filedialog.askopenfilename(title="Select the CSV file")

    df1 = pd.read_csv(file1_path)

    df1_split = pd.DataFrame([split_name(name) for name in df1['Name']], columns=['First', 'Middle', 'Last'])
    df1_split = pd.concat([df1_split, df1.drop(columns=['Name'])], axis=1)
    
    df1_split.to_csv("file1_split.csv", index=False)

    print("---Complete---")
    print(f"Output saved to file1_split.csv")

if __name__ == "__main__":
    main()
