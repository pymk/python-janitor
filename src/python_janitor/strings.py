from re import escape, sub
from unicodedata import combining, normalize

from src.python_janitor.utils import ALPHA_NUMERIC_SPACES, ASCII, LATIN


def strip_whitespace(s: str) -> str:
    """Remove leading and trailing whitespace from a string."""
    return s.strip()


def normalize_whitespace(s: str) -> str:
    """Replace all internal whitespace sequences with a single space."""
    return sub("\s+", " ", s.strip()).strip()


def remove_special_characters(s: str, keep: str = "") -> str:
    """Remove non-alphanumeric characters and spaces from a string.

    Args:
        s: Input string.
        keep: Additional characters to preserve (e.g. keep="-_").
    """
    to_rm = ALPHA_NUMERIC_SPACES
    if keep != "":
        position = to_rm.index("]")
        to_rm = to_rm[:position] + escape(keep) + to_rm[position:]

    return sub(to_rm, "", s)


def normalize_unicode(s: str) -> str:
    """
    Decompose unicode characters and strip accent marks, returning ASCII-safe text.
    Source: https://stackoverflow.com/a/71408065
    """
    outliers = str.maketrans(dict(zip(LATIN.split(), ASCII.split())))
    return "".join(
        c for c in normalize("NFD", s.translate(outliers)) if not combining(c)
    )


def to_snake_case(s: str) -> str:
    """Convert a string to snake_case (e.g. 'Hello World' -> 'hello_world')."""
    return sub("\s+", "_", s.lower().strip())


def to_kebab_case(s: str) -> str:
    """Convert a string to Kebab Case (e.g. 'hello world' -> 'hello-world')."""
    return sub("\s+", "-", s.lower().strip())


def to_pascal_case(s: str) -> str:
    """Convert a string to PascalCase (e.g. 'hello world' -> 'HelloWorld')."""
    return "".join(remove_special_characters(s).title().strip().split())


def to_camel_case(s: str) -> str:
    """Convert a string to camelCase (e.g. 'hello world' -> 'helloWorld')."""
    x = to_pascal_case(s)
    return "" if x == "" else x[0].lower() + x[1:]


def empty_to_none(s: str) -> str | None:
    """Return None if the string is empty or whitespace-only, otherwise return the string."""
    if not s or s.strip() == "":
        return None
    else:
        return s


def clean_string(
    s: str,
    *,
    unicode: bool = True,
    whitespace: bool = True,
    special_chars: bool = False,
    case: str | None = None,
) -> str:
    """Apply a configurable pipeline of cleaning steps to a string.

    Args:
        s: Input string.
        unicode: Whether to normalize unicode characters.
        whitespace: Whether to strip and normalize whitespace.
        special_chars: Whether to remove special characters.
        case: Target case style. One of 'snake', 'kebab', 'camel', 'pascal',
            'title', 'upper', 'lower', or None to skip.
    """
    x = s
    if unicode:
        x = normalize_unicode(x)
    if whitespace:
        x = normalize_whitespace(x)
    if special_chars:
        x = remove_special_characters(x)
        # removing special characters can create new whitespaces
        x = normalize_whitespace(x)
    if not case:
        return x
    match case:
        case "snake":
            x = to_snake_case(x)
        case "kebab":
            x = to_kebab_case(x)
        case "camel":
            x = to_camel_case(x)
        case "pascal":
            x = to_pascal_case(x)
        case "title":
            x = x.title()
        case "upper":
            x = x.upper()
        case "lower":
            x = x.lower()
        case _:
            raise ValueError(f"Unknown case: {case}")
    return x
