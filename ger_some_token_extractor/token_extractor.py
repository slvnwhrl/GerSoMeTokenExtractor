from collections.abc import Generator
from typing import Optional

import spacy

from .spacy_components import SoMaJoWrapper


class GerSoMeTokenExtractor:
    """Wrapper for a spacy pipline with custom components.

    Args:
        someweta_model_path (str): Path to the model for the SoMeWeTa component.
        split_sentences (bool): Whether sentences should be split (resulting in multiple lists, i.e., on list of tokens per sentence).
        remove_stopwords (bool): Wheter stopwords are removed from the output. Uses the spacy default stopwords for German (case insensitive).
        lowercase (bool): Wheter the returned tokens are lowercased. Defaults to False.
        lemmatize (bool): Whether the returned tokens are lemmatized. Defaults to False.
        remove_tokens (list[str], optional): A list of tokens that should be excluded (case sensitive).
        remove_pos (list[str], optional): A list of POS tags based on which tagged words should be excluded.
    """

    def __init__(
        self,
        someweta_model_path: str,
        split_sentences: bool = False,
        remove_stopwords: bool = True,
        lowercase: bool = False,
        lemmatize: bool = False,
        remove_tokens: Optional[list[str]] = None,
        remove_pos: Optional[list[str]] = None,
    ):
        nlp = spacy.blank("de")

        nlp.tokenizer = SoMaJoWrapper(
            vocab=nlp.vocab,
            language="de_CMC",
            split_sentences=split_sentences,
        )

        nlp.add_pipe(
            "SoMeWeTa",
            config={
                "model_path": someweta_model_path,
            },
        )
        nlp.add_pipe("TreeTagger")

        self.nlp = nlp

        self.lowercase = lowercase
        self.lemmatize = lemmatize
        self.remove_stopwords = remove_stopwords
        self.remove_tokens = (
            set(remove_tokens) if remove_tokens is not None else remove_tokens
        )
        self.remove_pos = set(remove_pos) if remove_pos is not None else remove_pos

    def _filter_text(self, doc: spacy.tokens.Doc) -> list[str]:
        """Filter a spacy Doc and return a Python list of str."""
        tokens = []
        for token in doc:
            if self.remove_stopwords and token.is_stop:
                continue
            elif self.remove_tokens is not None and token.text in self.remove_tokens:
                continue
            elif self.remove_pos is not None and token.tag_ in self.remove_pos:
                continue

            if self.lemmatize:
                token_text = token.lemma_
            else:
                token_text = token.text

            if self.lowercase:
                tokens.append(token_text.lower())
            else:
                tokens.append(token_text)

        return tokens

    def extract_text(self, text: str) -> list[str]:
        """Extracts tokens of a single text.

        Args:
            text (str): A single text to process.
        """
        return self._filter_text(self.nlp(text))

    def extract_texts(
        self, texts: list[str], n_process: int = 1, batch_size: int = 50
    ) -> Generator[list[str]]:
        """Extract multiple texts which are returned as a generator.
        Based on spacy's pipe method: https://spacy.io/api/language#pipe.

        Args:
            texts (list[str]): A list of texts to process.
            n_process (int): The number of processes used for parallelization. Defaults to 1.
            batch_size (int): The number of texts processed at once. Defaults to 50.
        """
        for text in self.nlp.pipe(texts, n_process=n_process, batch_size=batch_size):
            yield self._filter_text(text)
