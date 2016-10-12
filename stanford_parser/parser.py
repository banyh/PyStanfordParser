# -*- coding: utf-8 -*-
try:
    from jpype import startJVM, getDefaultJVMPath, shutdownJVM, java, JPackage, JString
    from zhconvert import ZHConvert
except:
    pass
from os.path import join, dirname

universal_tagset = {
    'AD': 'ADV',
    'AS': 'PRT',
    'BA': 'X',
    'CC': 'CONJ',
    'CD': 'NUM',
    'CS': 'CONJ',
    'DEC': 'PRT',
    'DEG': 'PRT',
    'DER': 'PRT',
    'DEV': 'PRT',
    'DT': 'DET',
    'ETC': 'PRT',
    'FW': 'X',
    'IJ': 'X',
    'JJ': 'ADJ',
    'LB': 'X',
    'LC': 'PRT',
    'M': 'NUM',
    'MSP': 'PRT',
    'NN': 'NOUN',
    'NR': 'NOUN',
    'NT': 'NOUN',
    'OD': 'NUM',
    'ON': 'X',
    'P': 'ADP',
    'PN': 'PRON',
    'PU': '.',
    'SB': 'X',
    'SP': 'PRT',
    'VA': 'VERB',
    'VC': 'VERB',
    'VE': 'VERB',
    'VV': 'VERB',
    'X': 'X',
}


class Parser(object):
    def __init__(self, lang='zh'):
        if lang == 'zh':
            try:
                self.zh = ZHConvert('http://localhost:9998/pos?wsdl', 'http://localhost:9999/seg?wsdl')
                self.zh.tw_postag(u'今天天氣真好')
            except:
                self.zh = ZHConvert()
        class_path = dirname(__file__)
        startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + class_path)
        Parser = JPackage('service').jpype.ParserJPype
        self.parser = Parser()
        self.parser.init(JString(lang))

    def __del__(self):
        shutdownJVM()

    def getParserResult(self, formatted_string):
        return self.parser.getParserResult(JString(formatted_string))

    def parse(self, sents):
        if isinstance(sents, basestring):
            sents = [sents]
        words = []
        tags = []
        orig_word_tag = []
        for sent in sents:
            tagtext = self.zh.tw_postag(sent)
            orig_word_tag.append(tagtext)
            words.append(' '.join([w for w, _ in tagtext]))
            tags.append(' '.join([t for _, t in tagtext]))
        word_tag = '$$$'.join(words) + '###' + '$$$'.join(tags)
        result = self.getParserResult(word_tag)

        list_of_nodes = []
        for sent, word_tag in zip(result.split('$$$'), orig_word_tag):
            sent_nodes = []
            relations = sent.split()
            j = 0
            last_parent = 0
            for i, (word, tag) in enumerate(word_tag):
                if tag == 'PU':
                    sent_nodes.append({
                        'id': i + 1,
                        'name': word,
                        'pos': universal_tagset[tag],
                        'ptb': tag,
                        'parent': last_parent,
                        'rel': 'punct',
                    })
                else:
                    rel = relations[j].split(',')
                    assert int(rel[2]) == i + 1
                    last_parent = int(rel[1])
                    sent_nodes.append({
                        'id': i + 1,
                        'name': word,
                        'pos': universal_tagset[tag],
                        'ptb': tag,
                        'parent': int(rel[1]),
                        'rel': rel[0],
                    })
                    j += 1
            list_of_nodes.append(sent_nodes)
        return list_of_nodes
