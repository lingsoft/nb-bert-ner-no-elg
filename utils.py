import os
from collections import defaultdict

from elg.model.base import Annotation
from transformers import pipeline

# NER pipeline that outputs token and NER, score
model_path = 'local_kb_bert_ner/' if os.path.isdir(
    'local_kb_bert_ner') else 'KB/bert-base-swedish-cased-ner'
print('model path', model_path)
ner = pipeline(
    task='ner',
    model=model_path,
    tokenizer=model_path,
    grouped_entities=True,
)


def is_exceed_limit(text):
    tokens = ner.tokenizer.tokenize(text)
    # max length is 512, max token length is 510. need to consider about\
    # [SOS] and [EOS]
    return len(tokens) > 510


def ner_func(text):
    ents = ner(text)
    last_index = 0
    # merge
    for ent in ents:
        if last_index == ent['start'] and last_index != 0:
            ent['entity'] = 'I-' + ent['entity_group']
        else:
            ent['entity'] = 'B-' + ent['entity_group']
        last_index = ent['end']
    ents = ner.group_entities(ents)
    output = defaultdict(list)
    for ent in ents:
        ent_group = ent.pop('entity_group')
        output[ent_group].append(
            Annotation(start=int(ent['start']),
                       end=int(ent['end']),
                       features={
                           "word": ent.pop('word'),
                           "score": str('%.3f' % ent.pop('score'))
                       }))
    return output
