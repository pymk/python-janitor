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


def _col_normalize_whitespace(df: pl.DataFrame) -> pl.DataFrame:
    """Strip leading and trailing whitespace and normalize internal whitespace in all column names."""
    return df.rename({col: normalize_whitespace(col) for col in df.columns})


def _col_apply_case(df: pl.DataFrame, case: CASING = "snake") -> pl.DataFrame:
    """Rename all columns to the requested casing."""
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


def _col_remove_special_characters(df: pl.DataFrame) -> pl.DataFrame:
    """Normalize unicode and remove special characters from all column names."""
    return df.rename(
        {col: remove_special_characters(normalize_unicode(col), keep="_-") for col in df.columns}
    )


def clean_dataframe(
    df: pl.DataFrame,
    *,
    case: CASING = "snake",
    ascii_only: bool = True,
) -> pl.DataFrame:
    """Apply a configurable pipeline of cleaning steps to a DataFrame.

    By default, leading and trailing whitespace from column names are stripped and
    internal whitespace is normalized.

    Args:
        df: Input DataFrame.
        case: Convert column names to "snake" (default), "kebab", "camel", or "pascal" casing.
        ascii_only: Whether to convert column names to ASCII-safe strings (default: True).
    """
    x = _col_normalize_whitespace(df)
    if ascii_only:
        x = _col_remove_special_characters(x)
    x = _col_apply_case(x, case=case)
    return x
