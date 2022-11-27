from fastai.vision.all import *
import csv
import glob
from collections import namedtuple
from pathlib import Path
csv_path = 'A/A/img_tag.csv'
a1_path = Path('A/A/A1')

# files = get_image_files(path)

a1_attr = 'path description'
A1Row = namedtuple('A1Row', a1_attr)


rows = []
path_to_tp = {}
train_images = []
train_images_set = set()

a1_attr = 'path description'
A1Row = namedtuple('A1Row', a1_attr)
csv_path = 'a1.csv'

rows = []
description_map = {}
A1_input = []

with open(csv_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for i, (partial_path, description) in enumerate(spamreader):
        if i == 0: continue
        path = Path('A/A/A1') / partial_path
        row = A1Row(path, description)
        rows.append(row)
        description_map[row.path.name] = row
        A1_input.append(row.path)

predict_images = []
for path in glob.glob(f'{a1_path}/**/*.tif', recursive=True):
    if path not in train_images_set:
        predict_images.append(Path(path))

def description_label(f):
    return description_map[f].description
path = Path('A/A/A1')


learn = load_learner(f'./purple/models/purple')
results = {}
for path in predict_images:
    results[path] = learn.predict(path)
    pred , _, _  = results[path]
    print(path, pred)
a1_attr = 'path description'
a1_header = a1_attr.split(' ')

with open('purple_pred.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(a1_attr)


    for path in predict_images:
        row = [path]
        pred , _, _  = results[path]
        print(path, pred)
        row.append(pred)
        writer.writerow(row)
