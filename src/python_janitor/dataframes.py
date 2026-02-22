from typing import Literal, get_args

import polars as pl

from src.python_janitor.strings import (
    normalize_unicode,
    normalize_whitespace,
    remove_special_characters,
    to_camel_case,
    to_kebab_case,
    to_pascal_case,
    to_snake_case,
)

CASING = Literal["snake", "kebab", "camel", "pascal"]


def col_normalize_whitespace(df: pl.DataFrame) -> pl.DataFrame:
    """Strip leading and trailing whitespace and normalize internal whitespace in all columns."""
    return df.rename({col: normalize_whitespace(col) for col in df.columns})


def col_clean_names(df: pl.DataFrame, case: CASING = "snake") -> pl.DataFrame:
    """Rename all columns to requested casing, stripping special characters and normalizing whitespace."""

    match case:
        case "snake":
            x = df.rename({col: to_snake_case(col) for col in df.columns})
        case "kebab":
            x = df.rename({col: to_kebab_case(col) for col in df.columns})
        case "camel":
            x = df.rename({col: to_camel_case(col) for col in df.columns})
        case "pascal":
            x = df.rename({col: to_pascal_case(col) for col in df.columns})
        case _:
            raise ValueError(f"Invalid case {case!r}. Expected one of: {get_args(CASING)}")
    return x


def col_remove_special_characters(df: pl.DataFrame) -> pl.DataFrame:
    """Remove special characters from all columns."""
    return df.rename({col: remove_special_characters(normalize_unicode(col)) for col in df.columns})


def clean_dataframe(
    df: pl.DataFrame,
    *,
    case: CASING = "snake",
    ascii_only: bool = True,
) -> pl.DataFrame:
    """Apply a configurable pipeline of cleaning steps to a DataFrame.

    By default, leading and trailing whitespace from column names are stripped. Additionally,
    internal whitespaces are normalize.

    Args:
        df: Input DataFrame.
        case: Convert to "snake" (default), "kebab", "camel", or "pascal" casing
        ascii_only: Whether to convert columns to ASCII-safe string (default: True)
    """
    x = col_normalize_whitespace(df)
    x = col_clean_names(x, case=case)
    if ascii_only:
        x = col_remove_special_characters(x)
    return x
