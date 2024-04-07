# Response for first chunk with no function_calling:
```py
{
  "generations": [
    [
      {
        "text": "#### S03L03 — Wyszukiwanie i bazy wektorowe\n\nW tej lekcji omówimy, dlaczego długoterminowa pamięć dla modelu jest jednym z najbardziej użytecznych zastosowań LLM. Omówione zostaną dwa główne powody:\n\n1. **Hiper-personalizacja** doświadczeń: to połączenie wiedzy na nasz temat z dostępem do usług i urządzeń. \n\n2. **Możliwość zbudowania częściowo autonomicznych zachowań**: to przekłada się na niespotykane wcześniej zastosowania.\n\nZobaczymy, jak te idee mogą być zastosowane w praktyce.\n\n## Czym są bazy wektorowe?\n\nBazy wektorowe to miejsce, gdzie przechowujemy i przeszukujemy dane po tokenizacji i embeddingu, które omówiliśmy w lekcji **C01L02**.\n\nZobaczmy na **uproszczoną wizualizację** wielowymiarowych danych, przedstawionych w przestrzeni 3D. [Kliknij tutaj, aby zobaczyć](https://projector.tensorflow.org).\n\n![](https://cloud.overment.com/word2vec-1695711060.gif)\n\nDzięki technikom porównywania wektorów, takim jak **cosine similarity**, możemy określić podobieństwo między danymi i odnaleźć te, które są do siebie zbliżone. \n\nPrzykładowo, na obrazku poniżej słowo **komputer** zostało powiązane ze słowami takimi jak **sprzęt, oprogramowanie, programowanie, pc, grafika, IBM czy Macintosh**.\n\n![](https://cloud.overment.com/cosine-cc650e6b-1.png)",
        "generation_info": {
          "finish_reason": "stop",
          "logprobs": None
        },
        "type": "ChatGeneration",
        "message": {
          "content": "#### S03L03 — Wyszukiwanie i bazy wektorowe\n\nW tej lekcji omówimy, dlaczego długoterminowa pamięć dla modelu jest jednym z najbardziej użytecznych zastosowań LLM. Omówione zostaną dwa główne powody:\n\n1. **Hiper-personalizacja** doświadczeń: to połączenie wiedzy na nasz temat z dostępem do usług i urządzeń. \n\n2. **Możliwość zbudowania częściowo autonomicznych zachowań**: to przekłada się na niespotykane wcześniej zastosowania.\n\nZobaczymy, jak te idee mogą być zastosowane w praktyce.\n\n## Czym są bazy wektorowe?\n\nBazy wektorowe to miejsce, gdzie przechowujemy i przeszukujemy dane po tokenizacji i embeddingu, które omówiliśmy w lekcji **C01L02**.\n\nZobaczmy na **uproszczoną wizualizację** wielowymiarowych danych, przedstawionych w przestrzeni 3D. [Kliknij tutaj, aby zobaczyć](https://projector.tensorflow.org).\n\n![](https://cloud.overment.com/word2vec-1695711060.gif)\n\nDzięki technikom porównywania wektorów, takim jak **cosine similarity**, możemy określić podobieństwo między danymi i odnaleźć te, które są do siebie zbliżone. \n\nPrzykładowo, na obrazku poniżej słowo **komputer** zostało powiązane ze słowami takimi jak **sprzęt, oprogramowanie, programowanie, pc, grafika, IBM czy Macintosh**.\n\n![](https://cloud.overment.com/cosine-cc650e6b-1.png)",
          "additional_kwargs": {},
          "response_metadata": {
            "token_usage": {
              "completion_tokens": 450,
              "prompt_tokens": 931,
              "total_tokens": 1381
            },
            "model_name": "gpt-4",
            "system_fingerprint": None,
            "finish_reason": "stop",
            "logprobs": None
          },
          "type": "ai",
          "name": None,
          "id": "run-75848fe8-dec7-4116-b23f-d001c4ef6662-0",
          "example": False
        }
      }
    ]
  ],
  "llm_output": {
    "token_usage": {
      "completion_tokens": 450,
      "prompt_tokens": 931,
      "total_tokens": 1381
    },
    "model_name": "gpt-4"
  },
  "run": [
    {
      "run_id": "75848fe8-dec7-4116-b23f-d001c4ef6662"
    }
  ]
}
```

# Response for first chunk with with function_calling:
```py
{
  "generations": [
    [
      {
        "text": "",
        "generation_info": {
          "finish_reason": "stop",
          "logprobs": None
        },
        "type": "ChatGeneration",
        "message": {
          "content": "",
          "additional_kwargs": {
            "function_call": {
              "arguments": "{\n\"content\": \"### Rozdział 3, Lekcja 3 - Wyszukiwanie i bazy wektorowe\\n\\nBazy wektorowe to miejsce, gdzie przechowujemy i przeszukujemy dane po tokenizacji i embeddingu. Służą do przechowywania wielowymiarowych danych, które możemy sobie wyobrazić jako punkty w przestrzeni 3D, co dobrze obrazuje [ten link](https://projector.tensorflow.org).\\n\\n![](https://cloud.overment.com/word2vec-1695711060.gif)\\n\\nDzięki porównywaniu wektorów możemy określić podobieństwo między nimi, co pomaga w odnajdywaniu zbliżonych danych. Przykładowo, wykorzystując metodę cosine similarity, otrzymujemy wartości od -1 (semantycznie odwrotne) do 1 (semantycznie powiązane). Na podstawie 'similarity score' baz wektorowych możemy wybrać te wpisy, które są najbardziej zbliżone semantycznie do naszego zapytania.\\n\\nNa poniższym obrazku widać, jak słowo 'komputer' zostało powiązane z innymi pokrewnymi słowami jak 'sprzęt', 'oprogramowanie', 'programowanie', 'pc', 'grafika', 'IBM' czy 'Macintosh'.\\n\\n![](https://cloud.overment.com/cosine-cc650e6b-1.png)\\n\\nDługoterminowa pamięć dla modelu jest jednym z najbardziej użytecznych zastosowań LLM, pozwalając na hiper-personalizację doświadczeń oraz możliwość zbudowania częściowo autonomicznych zachowań. \",\n\"tags\": [\"bazy wektorowe\", \"wyszukiwanie\", \"tokenizacja\", \"embedding\", \"podobieństwo semantyczne\", \"cosine similarity\", \"długoterminowa pamięć\", \"autonomiczne zachowania\"]\n}",
              "name": "summarization"
            }
          },
          "response_metadata": {
            "token_usage": {
              "completion_tokens": 494,
              "prompt_tokens": 1106,
              "total_tokens": 1600
            },
            "model_name": "gpt-4",
            "system_fingerprint": None,
            "finish_reason": "stop",
            "logprobs": None
          },
          "type": "ai",
          "name": None,
          "id": "run-93d51981-b33b-4d17-8c5d-56ba33b46df9-0",
          "example": False
        }
      }
    ]
  ],
  "llm_output": {
    "token_usage": {
      "completion_tokens": 494,
      "prompt_tokens": 1106,
      "total_tokens": 1600
    },
    "model_name": "gpt-4"
  },
  "run": [
    {
      "run_id": "93d51981-b33b-4d17-8c5d-56ba33b46df9"
    }
  ]
}
```