import pandas as pd 
import json
from tqdm import tqdm
import re

pattern = re.compile(r"\b(?:professor|prof\.?|doctor|dr\.?)\b\.?", re.IGNORECASE)

def clean_title(text):
    return re.sub(pattern, "", text).strip()

dataset = {
    'nodes':[],
    'links':[]
}

def add_node(node):
    if node not in dataset['nodes']:
        dataset['nodes'].append(node)

def process_csv(file):
    for _, row in tqdm(file.iterrows(), total=len(file), desc="Processing Rows", unit="row"):
        student = {"id" : row['Your Name'], 'group':'Student'}
        if student not in dataset['nodes']:
            dataset['nodes'].append(student)
        
        for x in ['Your Main Supervisor', 'Your Second Supervisor']:
            sup = {"id" : clean_title(row[x]), 'group':'Supervisor'}
            add_node(sup)
            if x == 'Your Main Supervisor':
                value = 3
            else:
                value = 1
            dataset['links'].append({ "source": row["Your Name"], "target":  clean_title(row[x]), "value": value })

        for x in [['Your Third Supervisor','Is your third supervisor industrial'], ['Your Fourth Supervisor','Is your fourth supervisor industrial']]:
            if pd.isna(row[x[0]]):
                break
            sup = {"id" :  clean_title(row[x[0]]), 'group':'Supervisor' if  pd.isna(row[x[1]]) or (row[x[1]] == 'No') else 'Industrial Supervisor'}
            add_node(sup)
            dataset['links'].append({ "source": row["Your Name"], "target":  clean_title(row[x].iloc[0]), "value": 1 })

        for x in ['Topic One', 'Topic Two', 'Topic Three']:
            topic = {"id" : row[x], 'group':'Topic'}
            add_node(topic)
            dataset['links'].append({ "source": row["Your Name"], "target": row[x], "value": 2 })

if __name__ == '__main__':
    file = pd.read_csv('KnowledgeGraphForm.csv')
    process_csv(file)
    with open("sample.json", "w") as outfile: 
        json.dump(dataset, outfile)
    
    