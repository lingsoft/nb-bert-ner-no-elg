from transformers import pipeline

ner = pipeline(
    task='ner',
    model='NbAiLab/nb-bert-base-ner',
    tokenizer='NbAiLab/nb-bert-base-ner',
    grouped_entities=True,
)
# Save pipeline
path = 'local_nb_bert_ner'
ner.save_pretrained(path)
