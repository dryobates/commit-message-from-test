import pytest

from cmft.utils import camel_to_snake, snake_to_words


@pytest.mark.parametrize(
    "text", ["snake_case", "snake__case", "_snake_case", "snake_case_"]
)
def test_returns_words_from_snake_case_text(text):
    words = snake_to_words(text)

    assert "snake case" == words


@pytest.mark.parametrize("text", ["CamelCase", "camelCase"])
def test_converts_camel_case_to_snake_case(text):
    result = camel_to_snake(text)

    assert "camel_case" == result
