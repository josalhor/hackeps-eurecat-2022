from fastai.vision.all import *
import csv
import glob
from collections import namedtuple
from pathlib import Path
csv_path = 'B/B/train.csv'
b2_path = Path('B/B/data')
path = b2_path

# files = get_image_files(path)

b2_attr = 'id path'
b2_pred = 'oil wide hole hor_fine2 hor_tense barring borrisol hor_fine pe'
BRow = namedtuple('BRow', b2_attr + ' ' + b2_pred)
b2_feat = b2_pred.split(' ')

rows = []
path_to_tp = {}
train_images = []
train_images_set = set()

rows = []
path_to_tp = {}
train_images = []

with open(csv_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        row[1] = Path('B/B/data') / Path(row[1])
        if not row[1].exists(): continue
        row = BRow(*row)
        pname = Path(row.path).name
        assert pname not in path_to_tp
        path_to_tp[pname] = row
        rows.append(row)
        train_images.append(Path(row.path))

predict_images = []
for path in glob.glob(f'{b2_path}/*.jpg', recursive=True):
    predict_images.append(Path(path))


train_tp = [
    ('oil'),
    ('wide'),
    ('hole'),
    ('hor_fine2'),
    ('hor_tense'),
    ('barring_fine'),
    ('borrisol_fine'),
    ('hor_fine'),
    ('pe'),
]

def oil_label(f):
    return path_to_tp[f].oil

def wide_label(f):
    return path_to_tp[f].wide

def hole_label(f):
    return path_to_tp[f].hole

def hor_fine2_label(f):
    return path_to_tp[f].hor_fine2

def barring_label(f):
    return path_to_tp[f].barring

def borrisol_label(f):
    return path_to_tp[f].borrisol


def hor_tense_label(f):
    return path_to_tp[f].hor_tense

def hor_fine_label(f):
    return path_to_tp[f].hor_fine

def pe_label(f):
    return path_to_tp[f].pe

results_by_type = {}

for pred_type in train_tp:
    learn = load_learner(f'./green/models/{pred_type}')
    results = {}
    for path in predict_images:
        results[path] = learn.predict(path)
    results_by_type[pred_type] = results

with open('green_pred.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(b2_feat)


    for i, path in enumerate(predict_images):
        print('Row', i / len(predict_images))
        row = [path]
        for pred_type in train_tp:
            pred , _, _  = results_by_type[pred_type][path]
            row.append(pred)
        writer.writerow(row)
