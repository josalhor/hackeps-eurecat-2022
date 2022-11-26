from fastai.vision.all import *
import csv
import glob
from collections import namedtuple
from pathlib import Path
csv_path = 'A/A/train-hackeps_a2.csv'
a2_path = Path('A/A/A2')

# files = get_image_files(path)

a2_attr = 'id1 id2 name path holes verticals horizontals others oil fringe'
A2Row = namedtuple('A2Row', a2_attr)
# print(len(files))
# input('w')

rows = []
path_to_tp = {}
train_images = []
train_images_set = set()

with open(csv_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:

        print(row)
        row = A2Row(*row)
        pname = Path(row.path).name
        assert pname not in path_to_tp
        path_to_tp[pname] = row
        rows.append(row)
        train_images.append(Path(row.path))
        train_images_set.add(row.path)

predict_images = []
for path in glob.glob(f'{a2_path}/**/*.tif', recursive=True):
    if path not in train_images_set:
        predict_images.append(Path(path))

train_tp = [
    ('holes'),
    ('verticals'),
    ('horizontals'),
    ('others'),
    ('oil'),
    ('fringe'),
]

results_by_type = {}

for pred_type in train_tp:
    learn = load_learner(f'/home/josalhor/Desktop/eurecat-2022/A/A/A2/{pred_type}')
    results = {}
    for path in predict_images:
        results[path] = learn.predict(path)
    results_by_type[pred_type] = results

a2_attr = 'path holes stripe oil creased frige others'
a2_header = a2_attr.split(' ')

with open('a2_pred.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(a2_header)


    for path in predict_images:
        row = [path]
        for pred_type in train_tp:
            row.append(
                results_by_type[pred_type][path]
            )
        writer.writerow(row)

print(results)