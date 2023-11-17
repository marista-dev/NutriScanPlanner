import yaml
from IPython.core.display_functions import display

data = { 'train' : './Ingre/train/images/',
         'val' : './Ingre/valid/images/',
         'test' : './Ingre/test/images',
         'names' : ['butter', 'egg', 'milk', 'onion', 'potato'],
         'nc' : 5 }

with open('./Ingre/Ingre.yaml', 'w') as f:
  yaml.dump(data, f)


with open('./Ingre/Ingre.yaml', 'r') as f:
  taco_yaml = yaml.safe_load(f)
  display(taco_yaml)

import ultralytics
print(ultralytics.checks())