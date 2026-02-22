from re import escape, sub
from unicodedata import category, combining, normalize

ALPHA_NUMERIC_SPACES = r"[^a-zA-Z0-9 ]+"
LATIN = "ä  æ  ǽ  đ ð ƒ ħ ı ł ø ǿ ö  œ  ß  ŧ ü  Ä  Æ  Ǽ  Đ Ð Ƒ Ħ I Ł Ø Ǿ Ö  Œ  ẞ  Ŧ Ü "
ASCII = "ae ae ae d d f h i l o o oe oe ss t ue AE AE AE D D F H I L O O OE OE SS T UE"


def _strip_whitespace(s: str) -> str:
    """Remove leading and trailing whitespace from a string."""
    return s.strip()


def normalize_whitespace(s: str) -> str:
    """Replace all internal whitespace sequences with a single space."""
    return sub(r"\s+", " ", s.strip()).strip()


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
    return "".join(c for c in normalize("NFD", s.translate(outliers)) if not combining(c))


def to_snake_case(s: str) -> str:
    """Convert a string to snake_case (e.g. 'Hello World' -> 'hello_world')."""
    x = _split_into_words(normalize_whitespace(s))
    return "_".join(x).lower().strip()


def to_kebab_case(s: str) -> str:
    """Convert a string to kebab-case (e.g. 'hello world' -> 'hello-world')."""
    x = _split_into_words(normalize_whitespace(s))
    return "-".join(x).lower().strip()


def to_pascal_case(s: str) -> str:
    """Convert a string to PascalCase (e.g. 'hello world' -> 'HelloWorld')."""
    x = _split_into_words(remove_special_characters(s.strip(), keep="_- "))
    return "".join([c.title() for c in x])


def to_camel_case(s: str) -> str:
    """Convert a string to camelCase (e.g. 'hello world' -> 'helloWorld')."""
    x = to_pascal_case(s)
    return "" if x == "" else x[0].lower() + x[1:]


def to_none_if_empty(s: str) -> str | None:
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


def _split_into_words(s: str) -> list[str]:
    """Split words based on camelCase, PascalCase, and whitespace boundaries."""
    words = []
    current_word = []

    for i, current_chr in enumerate(s):
        prev_chr = s[i - 1] if i > 0 else None
        next_chr = s[i + 1] if i < len(s) - 1 else None

        # If delimiter, save current word and skip the delimiter
        if _is_delimiter(current_chr):
            if current_word:
                words.append("".join(current_word))
                current_word = []
            continue

        # If camelCase boundary, save current word and start new one
        if _is_lower(prev_chr) and _is_upper(current_chr):
            if current_word:
                words.append("".join(current_word))
                current_word = []

        # If PascalCase, save word and start new
        if (
            0 < i < len(s) - 1
            and _is_upper(prev_chr)
            and _is_upper(current_chr)
            and _is_lower(next_chr)
        ):
            if current_word:
                words.append("".join(current_word))
                current_word = []

        current_word.append(current_chr)

    # Add the last word if current_word is not empty
    if current_word:
        words.append("".join(current_word))

    return words


def _is_delimiter(c: str) -> bool:
    """Return True for whitespace, underscores, and hyphens."""
    return c.isspace() or c in {"_", "-"}


def _is_upper(c: str | None) -> bool:
    """Return True for uppercase character."""
    return category(c) == "Lu" if c else False


def _is_lower(c: str | None) -> bool:
    """Return True for lowercase character."""
    return category(c) == "Ll" if c else False
