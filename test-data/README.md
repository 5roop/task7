# Test Data

## NOW corpus

This folder contains the sample of NOW (News on the Web) corpus (see https://www.english-corpora.org/now/) in the JSON format (list of dictionaries), where each element consists of the following attributes:
* "id" - text id,
* "words" - no. of words,
* "date",
* "country": "US",
* "website",
* "url",
* "title",
* "text": text as it was in the sample,
* "lower_text": lower-cased text, could be more useful for the lexicon

The NOW corpus contains the following no. of texts per English-speaking countries:
`GB    385
US    383
IN    380
CA    348
IE    267
ZA    196
AU    147
NG    129
NZ    120
PH    111
SG     97
PK     77
MY     71
GH     56
KE     32
BD     20
LK     16
JM     15
TZ      6
HK      5`

NOW-GB and NOW-US are corpora, extracted from the NOW-corpus-sample, containing only British or American texts.

## GloWBE and NOW corpus

Additionally, the NOW corpus has been enlarged by adding the GloWBE corpus - see the GloWBe-and-NOW-corpus-sample.json file. It has 724 GB texts and 721 US texts.

The JSON file has the same structure as described above, except it does not have the following attributes: `date` and `url`, and it has one additional attribute `corpus` for separating between texts from NOW and GloWBE.

The sample of GloWBE (Corpus of Global Web-Based English - see https://www.english-corpora.org/glowbe/) contains British and American text from general websites or blogs.