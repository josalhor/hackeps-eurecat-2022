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


def hole_label(f):
    return path_to_tp[f].holes

learn = load_learner('/home/josalhor/Desktop/eurecat-2022/A/A/A2/holes')
results = {}
for path in predict_images:
    results[path] = learn.predict(path)

print(results)