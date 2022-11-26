

csv_path = '/home/josalhor/Desktop/eurecat-2022/A/A/A1/img_tag.csv'
a1_path = '/home/josalhor/Desktop/eurecat-2022/A/A/A1'
import unicodedata
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

import csv

from collections import namedtuple

CSVRow = namedtuple('CSVRow', 'id c r e name path classification')
a2_attr = 'path holes stripe oil creased frige others'
A2Row = namedtuple('A2Row', a2_attr)
a2_header = a2_attr.split(' ')

rows = []

with open(csv_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        rows.append(
            CSVRow(*row)
        )

d = {
    ('c1', 'r1'): 'Fil unic - Tela fila - small knit',
    ('c1', 'r2'): 'RES',
    ('c1', 'r3'): 'Double fil - Tela fila - small knit',
    ('c2', 'r1'): 'RES',
    ('c2', 'r2'): 'Fil unic - Tela gruixuda - big knit',
    ('c2', 'r3'): 'Double fil - Tela gruixuda - big knit',
    ('c3', 'r1'): 'Quadres',
    ('c3', 'r2'): 'RES',
    ('c3', 'r3'): 'Files',
    ('c4', 'r1'): 'Burn-like',
    ('c4', 'r2'): 'RES',
    ('c4', 'r3'): 'Flower',
}

header = ['path', 'descritpion']

with open('a1.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for row in rows:
        pred = (row.c, row.r)
        description = d[pred]
        # write the data
        writer.writerow([row.path, description])


with open('a2.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(a2_header)

    for row in rows:
        clas = strip_accents(row.classification).lower().strip()
        hole = 'agujero' in clas
        crease = 'pliegue' in clas or 'doble en' in clas or ('arruga' in clas)
        fringe = 'franja' in clas
        stripe = 'raya' in clas
        wide = 'a lo largo' in clas
        mancha = 'mancha' in clas
        oil = 'aceite' in clas or 'grasa' in clas or 'corta' in clas
        other = mancha or (stripe and not wide) or ('hilo' in clas) or ('pelusa' in clas) or ('desgarro' in clas) or ('enhebre' in clas) or ('grieta' in clas) or ('salpicadura' in clas) or ('fallas' in clas)  or ('defecto' in clas) or ('pase la tela' in clas) or ('extranos' in clas) or ('pequeno' in clas or 'hoja de papel' in clas)
        not_error =  ('sombra' in clas) or \
                    (('lampara' in clas or 'luz' in clas) and \
                         'apagada' in clas) or \
                    ('desalineada' in clas and 'lampara' in clas) or \
                    (('distancia' in clas or 'inclinada' in clas) and \
                        'camara' in clas)
        all_errs = [hole, wide, oil, crease, fringe, other]
        any_err = any(all_errs)
        if clas and not any_err and not not_error:
            print('?', row.path, clas)
        as_binary = list(map(int, all_errs))
        row = [row.path] + as_binary
        writer.writerow(row)

# A2Row()