from fastai.vision.all import *
import csv
import glob
from collections import namedtuple
from pathlib import Path
csv_path = 'A/A/train-hackeps_a2.csv'
a2_path = Path('A/A/A2')
path = a2_path
# for path in glob.glob(f'{a2_path}/**/*.tif', recursive=True):
#     print(path)

# files = get_image_files(path)

a2_attr = 'id1 id2 name path holes verticals horizontals others oil fringe'
A2Row = namedtuple('A2Row', a2_attr)
# print(len(files))
# input('w')

rows = []
path_to_tp = {}
train_images = []

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

def hole_label(f):
    return path_to_tp[f].holes

def vertical_label(f):
    return path_to_tp[f].verticals

def horizontal_label(f):
    return path_to_tp[f].horizontals

def other_label(f):
    return path_to_tp[f].others

def oil_label(f):
    return path_to_tp[f].oil

def fringe_label(f):
    return path_to_tp[f].fringe

train_tp = [
    ('holes', hole_label),
    ('verticals', vertical_label),
    ('horizontals', horizontal_label),
    ('others', other_label),
    ('oil', oil_label),
    ('fringe', fringe_label),
]

for name, label_fn in train_tp:
    dls = ImageDataLoaders.from_name_func(path, train_images, label_fn, item_tfms=Resize(224))
    learn = vision_learner(dls, resnet34, metrics=error_rate)
    learn.fine_tune(10)
    learn.export(name)