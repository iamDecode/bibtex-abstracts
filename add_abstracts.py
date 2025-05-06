from pybtex.database import parse_file
from pybtex.richtext import String
import requests
from urllib.parse import quote

data = parse_file("test.bib", "bibtex")

for entry in data.entries.values():
  title = entry.fields.get('title', None)

  if title is None:
    continue

  print(f'processing paper: {title}')

  cleaned_title = title.replace(',', '').replace(':', '')
  encoded_title = quote(cleaned_title)
  url = f"https://api.openalex.org/works?filter=title.search:{encoded_title}"
  response = requests.get(url)
  
  if response.status_code == 200:
    json = response.json()
    results = json.get('results', [])

    abstract_dict: dict = next((r.get('abstract_inverted_index', None) for r in results if r.get('abstract_inverted_index', None) is not None))

    abstract_text = ' '.join(abstract_dict.keys())
    entry.fields['abstract'] = abstract_text
  else:
    print(f"Error: {response.status_code}")

data.to_file("new.bib")