# ELG API for BERT base fine-tuned for Norwegian NER

This git repository contains [ELG compatible](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) Flask based REST API for the BERT base fine-tuned for Norwegian NER

[Norwegian Transformer Model](https://github.com/NBAiLab/notram) contains information about the available open-source corpus and pre-trained models that can be fine-tuned for NLP tasks. This API was developed based on the fine-tuned version of `nb-bert-base` on [NbAilab/norne](https://github.com/ltgoslo/norne) dataset, Bokmaal data part. The data can be loaded from HuggingFace library and is published under `CC0` License.
Original author: National Library of Norway, published under `Apache-2.0` License.


This ELG API was developed in EU's CEF project: [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry)

## Local development

Setup virtualenv, dependencies
```
python3 -m venv nb-ner-elg-venv
source nb-ner-elg-venv/bin/activate
python3 -m pip install -r requirements.txt
```

For direct use, the [latest](https://huggingface.co/NbAiLab/nb-bert-base-ner)(17.11.2021) model is a fine-tuned version for NER task using the [NorNE](https://huggingface.co/datasets/NbAiLab/norne) dataset. The model is published under cc-by-4.0 license. To load the fine-tuned model into the local directory `local_nb_bert_ner`

```
python3 load_model.py
```

Optionally, one may want to fine-tune a pre-trained model. For that, the pre-trained model `nb-bert-base` is available in Huggingface, and [here](https://colab.research.google.com/gist/peregilk/6f5efea432e88199f5d68a150cef237f/-nbailab-finetuning-and-evaluating-a-bert-model-for-ner-and-pos.ipynb) is the Google Colab to fine-tune it. The model once trained can be also used locally by saving the model to the local disk, script to save the trained model is available at the final cell in the same colab. Below we provide the fine-tuning configuraiton parameters that we used.

### Fine Tune Parameters
| Params | values |
|-|-| 
| base model | NbAiLab/nb-bert-base |
| train data | bokmaai |
| learning rate | 3e-5 |
| train epochs | 4 |
| warm up steps | 750 | 



Run the development mode flask app
```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

## Building the docker image

```
docker build -t nb-ner-elg .
```

Or pull directly ready-made image `docker pull lingsoft/nb-bert-ner-no/:tagname`.

## Deploying the service

```
docker run -d -p <port>:8000 --init --memory="2g" --restart always nb-ner-elg
```

## REST API

### Call pattern

#### URL

```
http://<host>:<port>/process
```

Replace `<host>` and `<port>` with the hostname and port where the 
service is running.

#### HEADERS

```
Content-type : application/json
```

#### BODY

For text request
```
{
  "type":"text",
  "content": text to be analyzed for NER task
}
```
#### RESPONSE

```
{
  "response":{
    "type":"annotations",
    "annotations":{
      "<NER notation>":[ // list of tokens that were recognized
        {
          "start":number,
          "end":number,
          "features":{ "word": str, "score": float }
        },
      ],
    }
  }
}
```

### Response structure

- `start` and `end` (int)
  - the indices of the token in the send request
- `word` (str)
  - word/phrase that is recognized with entities
- `score` (float)
  - confidence score of the entity, log likelihood probability.

### Example call

```
curl -d '{"type":"text","content":"Svein Arne Brygfjeld, Freddy Wetjen, Javier de la Rosa og Per E Kummervold jobber alle ved AILABen til Nasjonalbiblioteket. Nasjonalbiblioteket har lokaler både i Mo i Rana og i Oslo."}' -H "Content-Type: application/json" -X POST http://localhost:8000/process
```

### Response should be

```json
{
  "response": {
    "type": "annotations",
    "annotations": {
      "PER": [
        {
          "start": 0,
          "end": 20,
          "features": {
            "word": "Svein Arne Brygfjeld",
            "score": "1.000"
          }
        },
        {
          "start": 22,
          "end": 35,
          "features": {
            "word": "Freddy Wetjen",
            "score": "1.000"
          }
        },
        {
          "start": 37,
          "end": 54,
          "features": {
            "word": "Javier de la Rosa",
            "score": "0.994"
          }
        },
        {
          "start": 58,
          "end": 74,
          "features": {
            "word": "Per E Kummervold",
            "score": "1.000"
          }
        }
      ],
      "DRV": [
        {
          "start": 91,
          "end": 92,
          "features": {
            "word": "A",
            "score": "0.828"
          }
        }
      ],
      "ORG": [
        {
          "start": 103,
          "end": 122,
          "features": {
            "word": "Nasjonalbiblioteket",
            "score": "0.997"
          }
        },
        {
          "start": 124,
          "end": 143,
          "features": {
            "word": "Nasjonalbiblioteket",
            "score": "0.994"
          }
        }
      ],
      "GPE_LOC": [
        {
          "start": 163,
          "end": 172,
          "features": {
            "word": "Mo i Rana",
            "score": "0.989"
          }
        },
        {
          "start": 178,
          "end": 182,
          "features": {
            "word": "Oslo",
            "score": "0.999"
          }
        }
      ]
    }
  }
}
```

## Comparision of fine-tuned version from `NbAiLab/nb-bert-base-ner` and our own fine-tuned version based on `NbAiLab/nb-bert-base`
| NER bert model               | configurations                                         | data for testing   | Eval F1 score |
|------------------------------|--------------------------------------------------------|--------------------|---------------|
|  fine-tuned based on nb-bert |  see [Table](#fine-tune-parameters)                                                       |bokmål train        | **0.99847**  |
|                              |                                                         | bokmål test        | 0.91117      |
|                              |                                                        | bokmål validation  | **0.93700**   |
|                              |                                                        | Nynorsk train      | 0.90097       |
|                              |                                                        | Nynorsk test       | **0.87628**   |
|                              |                                                        | Nynorsk validation | **0.91458**   |
|  NbAiLab/nb-bert-base-ner    |  fine-tuned already                                    | bokmål train       | 0.99386       |
|                              |                                                        | bokmål test        | **0.91222**   |
|                              |                                                        | bokmål validation  | 0.93247       |
|                              |                                                        | Nynorsk train      | **0.90335**  |
|                              |                                                        | Nynorsk test       | 0.87568       |
|                              |                                                        | Nynorsk validation | 0.90251       |
