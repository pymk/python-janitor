import polars as pl

from src.python_janitor import (
    clean_dataframe,
    clean_string,
    normalize_unicode,
    normalize_whitespace,
    remove_special_characters,
    to_camel_case,
    to_kebab_case,
    to_none_if_empty,
    to_pascal_case,
    to_snake_case,
)

print(normalize_whitespace("hello   world"))  # "hello world"
print(normalize_unicode("café"))  # "cafe"
print(remove_special_characters("hello, world!"))  # "hello world"
print(to_snake_case("hello world"))  # "hello_world"
print(to_kebab_case("hello world"))  # "hello-world"
print(to_pascal_case("hello world"))  # "HelloWorld"
print(to_camel_case("hello world"))  # "helloWorld"
print(to_none_if_empty("   "))  # None

print(clean_string("  héllo   wörld  "))  # "hello woerld"
print(clean_string("café", unicode=False))  # "café"
print(clean_string("hello   world", whitespace=False))  # "hello   world"
print(clean_string("hello, world!", special_chars=True))  # "hello world"

df = pl.DataFrame({"  Hello World  ": [1, 2], "fooBar": [3, 4], "café_col": [5, 6]})
print(clean_dataframe(df))
print(clean_dataframe(df, case="pascal"))
print(clean_dataframe(df, ascii_only=False))
