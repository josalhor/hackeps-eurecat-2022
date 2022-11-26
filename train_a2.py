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


def plot_metrics(name, self: Recorder, nrows=None, ncols=None, figsize=None, **kwargs):
    metrics = np.stack(self.values)
    names = self.metric_names[1:-1]
    n = len(names) - 1
    if nrows is None and ncols is None:
        nrows = int(math.sqrt(n))
        ncols = int(np.ceil(n / nrows))
    elif nrows is None: nrows = int(np.ceil(n / ncols))
    elif ncols is None: ncols = int(np.ceil(n / nrows))
    figsize = figsize or (ncols * 6, nrows * 4)
    fig, axs = subplots(nrows, ncols, figsize=figsize, **kwargs)
    axs = [ax if i < n else ax.set_axis_off() for i, ax in enumerate(axs.flatten())][:n]
    for i, (name, ax) in enumerate(zip(names, [axs[0]] + axs)):
        ax.plot(metrics[:, i], color='#1f77b4' if i == 0 else '#ff7f0e', label='valid' if i > 0 else 'train')
        ax.set_title(name if i > 1 else 'losses')
        ax.legend(loc='best')
    plt.savefig(f'{name}.png')

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
    learn.fine_tune(5)
    plot_metrics(name, learn.recorder)
    learn.export(name)