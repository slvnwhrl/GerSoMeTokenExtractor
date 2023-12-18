## Introdcution
This repository provides a token extractor for German social media texts. The extractor can be used to reduce texts to a list of selected (e.g., with a specific POS tag or a) and/or standardized (e.g., lemmatized). This can be useful, for instance, for topic modeling.

The code is based on a spacy pipeline with custom components that are especially suited for German social media texts. The choices for the components are partially motivated by this analysis: [Evaluating Off-the-Shelf NLP Tools for German](https://github.com/rubcompling/konvens2019). 

More specifically, it uses the following components:
- [SoMaJo](https://github.com/tsproisl/SoMaJo) for tokenization
- [SoMeWeTa](https://github.com/tsproisl/SoMeWeTa) for POS-tagging
- [TreeTagger](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) for lemmatization

## Installation
To install this repository, run the following code:
```
https://github.com/slvnwhrl/GerSoMeTokenExtractor.git
cd GerSoMeTokenExtractor
pip install .
# or pip install -e . for an editable install
```

And also make sure that you have installed all dependencies:
- SoMeWeTa: you have to download a model [here](https://github.com/tsproisl/SoMeWeTa#model-files). Alterantively, you can train a model yourself. Please also have a look at the license of the models (e.g., the "German web and social media" model should only be used for research).
- TreeTagger: follow the instructions for the German model [here](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/).

## Usage
To use the extractor, you simple have to import and instantiate the [GerSoMeTokenTextractor class](https://github.com/slvnwhrl/GerSoMeTokenExtractor/blob/2b8a980b28e4cb377c8b1a6628ab4b1e4977141e/ger_some_token_extractor/token_extractor.py#L9C11-L9C11):

```
from ger_some_token_extractor import GerSoMeTokenExtractor

someweta_model_path = "path/to/the/model"

# This might take a couple of seconds to load all the components.
extractor = GerSoMeTokenExtractor(
    someweta_model_path,
    lowercase=True,
    lemmatize=True,
    remove_pos=["$,", "$(", "$."]
)

sentences = [
    "Das ist ein Test... Cool, oder?;)",
    "Guten Nacht\n\n\n🪐💫⭐️",
]

# This processes a single text.
print(extractor.extract_text(sentences[0]))
# Output: ['test', 'cool', ';)']

# This processes a list of texts.
for tokens in extractor.extract_texts(sentences):
    print(tokens)
# Output: ['test', 'cool', ';)'], ['gut', 'nacht', '🪐', '💫', '⭐️']
```

The `GerSoMeTokenExtractor` can be instantiated with a couple of parameters:
| **attribute**                       | **description**                                                                                               |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------|
| someweta_model_path (str)           | Path to the model for the SoMeWeTa component.                                                                 |
| split_sentences (bool)              | Whether sentences should be split (resulting in multiple lists, i.e., on list of tokens per sentence).        |
| remove_stopwords (bool)             | Wheter stopwords are removed from the output. Uses the spacy default stopwords for German (case insensitive). |
| lowercase (bool)                    | Wheter the returned tokens are lowercased. Defaults to False.                                                 |
| lemmatize (bool)                    | Whether the returned tokens are lemmatized. Defaults to False.                                                |
| remove_tokens (list[str], optional) | A list of tokens that should be excluded (case sensitive).                                                    |
| remove_pos (list[str], optional)    | A list of POS tags based on which tagged words should be excluded.                                            |

**Note that the POS tags depend on the used model. For instance, SoMeWeTa's German web and social media model uses the [Tiger schema](https://www.linguistik.hu-berlin.de/de/institut/professuren/korpuslinguistik/mitarbeiter-innen/hagen/STTS_Tagset_Tiger).**

## Credits
If you use this library, please also make sure to give credits to the authors of the libraries on which the custom spacy components in this library are built! --> [SoMaJo](https://github.com/tsproisl/SoMaJo), [SoMeWeTa](https://github.com/tsproisl/SoMeWeTa), [TreeTagger](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/). And also make sure that you respect the respective licenses.
