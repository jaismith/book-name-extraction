import csv
from datetime import datetime
import random
import json
import re
import numpy as np

# magic number - count of books in books.csv (should have equal
# number of pos and neg samples)
NUM_SAMPLES = 11707

# remove list prefixing, leading/trailing spaces, replace all duplicate spaces
# with single spaces, remove all punctuation except .,$
def standardize(s):
  content = re.match(r'[0-9]?[.)]?(?:\\u2022)?\s?(.*)', s).groups()[0]
  content = re.sub('\s+', ' ', content)
  content = content.strip()
  return re.sub(r'[^\w\s.,$]+', '', content)

# segments starting with 'by' or 'isbn' are appended to previous segment
def rule_based_clumping(samples):
  samples = iter(samples)

  output = [next(samples, None)]
  curr = next(samples, None)

  while curr is not None:
    if curr.lower().startswith(('by', 'isbn')):
      output[-1] += f' {curr}'
    else:
      output.append(curr)

    curr = next(samples, None)

  return output

# uses https://www.kaggle.com/jealousleopard/goodreadsbooks/download (download
# and place csv file in data/raw before running)
def generate_positive():
  # open and load csv
  file = open('data/raw/books.csv')
  data = csv.reader(file)

  # open and load pre-tagged positive data
  pretagged_pos_file = open('data/pretagged/positive.json')
  pretagged_pos_data = json.loads(pretagged_pos_file.read())

  # extract rows (throw away headers)
  rows = list(data)[1:]

  fields = {
    'title': 8,
    'authors': 4,
    'year': 2,
    'publisher': 2,
    'num_pages': 1,
    'isbn': 1,
    'price': 1
  }

  # generate samples
  samples = pretagged_pos_data + ([None] * len(rows))

  # warning if mismatched num samples
  if (len(samples) != NUM_SAMPLES):
    print(f'WARNING: NUM_SAMPLES magic number does not match the positive samples\n\tNUM_SAMPLES: {NUM_SAMPLES}, ACTUAL_SAMPLES: {len(samples)}')

  for i in range(len(rows)):
    title = rows[i][1]
    authors = rows[i][2].replace('/', ' ')
    num_pages = rows[i][7]
    year = None
    try:
      year = datetime.strptime(rows[i][10], "%m/%d/%Y").year
    except:
      year = random.randint(1800, 2021)
    publisher = rows[i][11]
    isbn10 = random.randint(10 ** 9, 10 ** 10 - 1)
    isbn13 = random.randint(10 ** 12, 10 ** 13 - 1)
    price = random.randint(10, 210)

    # select fields
    num_fields = random.randint(2, len(fields.keys()))
    random_fields = list(np.random.choice(list(fields.keys()), num_fields, replace=False, p=(np.array(list(fields.values())) * 1 / sum(fields.values()))))
    random_fields.sort(reverse=True, key=lambda field: fields[field])

    # generate format string (TODO: optimize?)
    sample = []
    for j in range(num_fields):
      if random_fields[j] == 'title': sample.append(f'{title}')
      if random_fields[j] == 'authors':
        if j == 0: sample.append(f'{authors}')
        else: sample.append(f'by {authors}')
      if random_fields[j] == 'num_pages': sample.append(f'{num_pages} pages')
      if random_fields[j] == 'year': sample.append(f'{year}')
      if random_fields[j] == 'publisher': sample.append(f'{publisher}')
      if random_fields[j] == 'isbn':
        if random.random():
          if random.random(): sample.append(f'isbn10 {isbn10}')
          else: sample.append(f'{isbn10}')
        else:
          if random.random(): sample.append(f'isbn13 {isbn13}')
          else: sample.append(f'{isbn13}')
      if random_fields[j] == 'price': sample.append(f'${price}')

    samples[i + len(pretagged_pos_data)] = sample[0]
    for s in sample[1:]:
      prefix = ',' if random.random() > 0.65 else ''
      samples[i + len(pretagged_pos_data)] += f'{prefix} {s}'

  print('Generated {} positive samples'.format(len(samples)))

  random.shuffle(samples)

  divider = int(len(samples) * .85)

  for (start, end, type) in [(0, divider, 'train'), (divider, len(samples), 'test')]:
    for i in range(start, end):
      output = open('data/processed/{}/positive/sample-{}.txt'.format(type, i), 'w')
      if (samples[i] is None): print(i)
      output.write(standardize(samples[i]))

def generate_negative():
  # load orc
  orc = json.loads(open('data/raw/orc.json').read())

  # open and load pre-tagged positive data
  pretagged_neg_file = open('data/pretagged/negative.json')
  pretagged_neg_data = json.loads(pretagged_neg_file.read())

  # extract descriptions (will generate 'negative' samples from this,
  # as it representative of the type of text textbook names are commonly
  # embedded in)
  descriptions = list(value['description'] for value in orc.values())

  def get_sample():
    sentences = re.split(r'[.?!;:]', random.choice(descriptions))
    sample = standardize(random.choice(sentences))

    if len(sample) > 0:
      return sample
    else:
      return get_sample()

  divider = int(NUM_SAMPLES * .85)

  samples = pretagged_neg_data + ([None] * (NUM_SAMPLES - len(pretagged_neg_data)))
  for i in range(len(pretagged_neg_data), NUM_SAMPLES):
    samples[i] = get_sample()

  print('Generated {} negative samples'.format(len(samples)))

  random.shuffle(samples)

  for (start, end, type) in [(0, divider, 'train'), (divider, NUM_SAMPLES, 'test')]:
    for i in range(start, end):
      output = open('data/processed/{}/negative/sample-{}.txt'.format(type, i), 'w')
      output.write(samples[i].strip())
