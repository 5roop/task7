# Test Data - NOW corpus

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