# imports
from requests import get

# fetch raw data (save to data/ folder)
def fetch_source(source_url, filename):
  res = get(source_url + filename)

  file = open('data/raw/' + filename, 'w')
  file.write(res.text)

def fetch_text_data(links):
  print('Fetching text data')

  links = list(links)

  text = []
  for i in range(len(links)):
    text.append(get(links[i]).text if links[i] is not None else 'n/a')
    print('\r{:2.2f}%'.format(i / len(links) * 100), end='')

  print()
  return text
