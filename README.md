# A Python Package for Stanford Parser

## Installation

```shell-script
pip install git+ssh://git@github.com/livingbio/PyStanfordParser.git#egg=PyStanfordParser
```

## Usage

Support languages: `'zh'`, `'en'`, `'fr'`, `'de'`.

```python
from stanford_parser import Parser
p = Parser('zh')
# [main] INFO edu.stanford.nlp.parser.lexparser.LexicalizedParser - Loading parser from serialized file edu/stanford/nlp/models/lexparser/chineseFactored.ser.gz ...
# done [6.3 sec].
p.parse(u'今天天氣真好')
# [[{'id': 1,
#    'name': u'\u4eca\u5929',
#    'parent': 3,
#    'pos': 'NOUN',
#    'ptb': u'NT',
#    'rel': u'tmod'},
#   {'id': 2,
#    'name': u'\u5929\u6c23',
#    'parent': 3,
#    'pos': 'NOUN',
#    'ptb': u'NN',
#    'rel': u'nsubj'},
#   {'id': 3,
#    'name': u'\u771f\u597d',
#    'parent': 0,
#    'pos': 'VERB',
#    'ptb': u'VV',
#    'rel': u'root'}]]
```
