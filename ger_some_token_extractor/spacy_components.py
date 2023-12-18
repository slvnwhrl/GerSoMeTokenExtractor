import warnings

import numpy as np

# This disables FutureWarnings from compiling regex expressions.
with warnings.catch_warnings():
    warnings.simplefilter(action="ignore", category=FutureWarning)
    import treetaggerwrapper

from somajo import SoMaJo
from someweta import ASPTagger
from spacy import Vocab
from spacy.lang.de import German
from spacy.language import Language
from spacy.symbols import LEMMA, TAG
from spacy.tokens import Doc


class SoMaJoWrapper(SoMaJo):
    """Wrapper for using the SoMaJo tokenizer (https://github.com/tsproisl/SoMaJo) with a spacy pipeline
    (https://spacy.io/usage/linguistic-features#custom-tokenizer-example)."""

    def __init__(
        self,
        vocab: Vocab,
        language: str = "de_CMC",
        **kwargs,
    ):
        super().__init__(language, **kwargs)

        self.vocab = vocab

    def __call__(self, text: str) -> Doc:
        words, spaces = [], []
        for sentence in self.tokenize_text([text]):
            for token in sentence:
                words.append(token.text)

                space_follows = True if "SpaceAfter=Yes" in token.extra_info else False
                spaces.append(space_follows)

        return Doc(self.vocab, words=words, spaces=spaces)


@German.factory("SoMeWeTa")
def someweta_factory(nlp: Language, name: str, model_path: str):
    """Factory function for creating a tokenizer based on SoMaJo (https://github.com/tsproisl/SoMaJo).
    Implementation based on https://spacy.io/usage/processing-pipelines#wrapping-models-libraries.
    """
    asptagger = ASPTagger()
    asptagger.load(model_path)

    def someweta_component(doc: Doc) -> Doc:
        tags = [
            doc.vocab.strings.add(tag[-1])
            for tag in asptagger.tag_sentence([token.text for token in doc])
        ]
        tags = np.array(tags, dtype="uint64")

        doc.from_array([TAG], tags)

        return doc

    return someweta_component


@German.factory("TreeTagger")
def treetagger_factory(nlp: Language, name: str):
    """Factory function for creating tagger based on TreeTagger (https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/).
    Implementation based on https://spacy.io/usage/processing-pipelines#wrapping-models-libraries.
    """
    treetagger = treetaggerwrapper.TreeTagger(TAGLANG="de")

    def treetagger_component(doc: Doc) -> Doc:
        def extract_lemma(tag: str):
            return tag.split("\t")[-1]

        lemmas = [
            doc.vocab.strings.add(extract_lemma(tag))
            for tag in treetagger.tag_text([token.text for token in doc], tagonly=True)
        ]
        lemmas = np.array(lemmas, dtype="uint64")

        doc.from_array([LEMMA], lemmas)

        return doc

    return treetagger_component
