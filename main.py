# imports
import json
from os.path import isfile
from bs4 import BeautifulSoup
# import spacy

import constants
from modules import loader, tagger, preprocessing

# download source data
# FILENAMES = [constants.TIMETABLE_FILENAME, constants.ORC_FILENAME]
# for filename in FILENAMES:
#   if not isfile('data/raw/' + filename):
#     loader.fetch_source(constants.DATA_SOURCE, filename)

# load into dictionaries
timetable = json.loads(open('data/raw/timetable.json').read())

# get text field links
text_data = None
if not isfile('data/raw/source.json'):
  links = (course['text'] for course in timetable.values())
  text = loader.fetch_text_data(links)

  text_data = json.dumps(text)
  open('data/raw/source.json', 'w').write(text_data)
else:
  text_data = json.loads(open('data/raw/source.json', 'r').read())

# parse text from links
data = []
for snippet in text_data:
  soup = BeautifulSoup(snippet, 'html.parser')
  segments = filter(
    lambda s:
      not s.startswith('Textbook information not yet submitted by department/program for ') and
      not s.startswith('Textbook(s) Required for '),
    soup.get_text(separator='<<AND>>', strip=True).split('<<AND>>')
  )

  data += list(preprocessing.standardize(segment) for segment in segments)

data = preprocessing.rule_based_clumping(data)

labels = [True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False, True, True, True, True, False, True, True, False, True, True, False, True, True, False, True, True, True, True, True, True, True, True, True, False, False, True, False, True, True, False, True, False, True, True, False, True, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, False, True, True, False, True, True, False, True, False, True, True, True, False, True, False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, True, False, False, False, False, True, False, True, True, False, False, True, True, False, False, True, True, False, False, True, False, False, False, True, True, False, True, False, False, False, False, False, True, True, True, True, True, False, False, False, False, False, True, True, True, True, True, False, True, False, False, True, True, True, True, False, False, False, True, True, True, True, True, False, False, True, True, True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, True, True, True, True, False, False, True, True, True, False, True, True, False, True, True, True, True, True, False, True, True, True, False, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, False, True, False, True, False, True, False, True, False, True, True, False, True, True, True, False, False, True, False, False, False, True, False, False, True, True, True, False, True, False, False, False, True, False, False, True, False, True, False, True, False, True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, False, True, False, True, True, True, False, True, False, False, False, True, True, True, True, False, False, True, True, True, False, True, True, True, False, True, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False, True, True, False, True, True, False, False, True, True, False, False, True, True, False, False, False, False, True, True, True, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False, True, True, True, True, False, True, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, False, True, True, True, True, True, False, True, True, True, True, True, False, False, False, True, False, False, True, True, True, True, False, True, False, False, False, False, False, False, True, True, False, True, False, False, True, False, False, False, False, False, True, True, False, False, True, True, False, True, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, True, True, False, True, True, False, True, True, False, True, True, True, False, True, True, True, True, False, True, True, True, False, False, True, True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False, True, False, True, True, True, True, True, True, False, True, True, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, True, False, True, False, True, False, False, False, True, False, False, True, True, False, False, True, True, False, False, True, True, False, True, False, True, False, True, True, True, True, True, True, False, True, True, True, False, False, True, False, False, False, False, False, True, False, False, True, False, True, False, True, False, True, False, True, False, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, True, False, True, True, True, True, False, True, True, False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, False, False, True, True, True, False, True, True, False, False, True, True, False, True, True, False, True, True, False, False, True, True, False, False, False, True, True, False, True, True, False, True, True, False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, True, True, False, False, False, False, False, False, True, True, False, True, True, False, True, True, False]

STARTER_POS = []
STARTER_NEG = []
for i in range(702, 702 + len(labels)):
  if labels[i - 702]:
    STARTER_POS.append(data[i])
  else:
    STARTER_NEG.append(data[i])

f_pos = open('f_pos.json', 'w')
f_pos.write(json.dumps(STARTER_POS))
f_neg = open('f_neg.json', 'w')
f_neg.write(json.dumps(STARTER_NEG))

# preprocessing.generate_positive()

# start = input(f'Enter starting index for tagging (0 - {len(data)}): ')
# print(tagger.tag(data, int(start)))

# for snippet in data[:100]:
#   print(snippet, end='\n\nREQUIREMENT\n')

# * TESTING

# data = ['Recommended, but not required:', 'Cell and Molecular Biology: Concepts and Experiments, 7th or 8th Edition', 'by Gerald Karp', 'The older 7th edition is adequate, and you may be able to find a used copy for sale.', 'For the 8th edition, only two purchase options are available.', 'Wiley E-text', 'Cell and Molecular Biology: Concepts and Experiments, 8th Edition', 'ISBN : 978-1-118-88384-6', '832 pages', 'January 2016, \\u00A92016', '(Note: there may be limitations as to how long you may be allowed to access the e-text, and how many pages you may print.)', 'Loose-leaf', 'Cell and Molecular Biology: Concepts and Experiments, Binder Ready Version, 8th Edition', 'ISBN : 978-1-118-88614-4', '832 pages', 'December 2015, \\u00A92016', 'An important note about the textbook:  We are not requiring that you purchase the textbook.   Exams will only cover material presented in class.  The textbook can be used as a reference to help clarify your understanding of material we discuss in class.   Some students find this very helpful, other students don\\u2019t use the textbook at all.  In deciding whether or not to purchase the textbook, consider what study strategies are most productive for you. Also, if you intend to apply to med school, vet school or graduate school then you may find having the text will be useful as a familiar source of information when you begin to review what you have learned in preparation for the MCAT or GRE exams.']

# nlp = spacy.load('en_core_web_sm')

# for seg in data:
#   doc = nlp(seg)
#   print('TEXT: \'{}\':\n\tENTS: {}\n\tNOUN_CHUNKS: {}'.format(seg, list(ent.text for ent in doc.ents), list(chunk.text for chunk in doc.noun_chunks)))
