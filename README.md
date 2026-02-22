# README

Python string clean-up tool.

## Examples

See [examples.py](./examples.py).

```python
normalize_whitespace("hello   world")              # "hello world"
normalize_unicode("café")                          # "cafe"

remove_special_characters("hello, world!")         # "hello world"

to_snake_case("hello world")                       # "hello_world"
to_kebab_case("hello world")                       # "hello-world"
to_pascal_case("hello world")                      # "HelloWorld"
to_camel_case("hello world")                       # "helloWorld"
to_none_if_empty("   ")                            # None

clean_string("  héllo   wörld  ")                  # "hello woerld"
clean_string("café", unicode=False)                # "café"
clean_string("hello   world", whitespace=False)    # "hello   world"
clean_string("hello, world!", special_chars=True)  # "hello world"

clean_dataframe(df)
clean_dataframe(df, case="pascal")
clean_dataframe(df, ascii_only=False)
```

## Structure

```
string-janitor/
├── pyproject.toml
├── README.md
├── .python-version
├── src/
│   └── string_janitor/
│       ├── __init__.py
│       ├── strings.py       # String cleaning functions
│       └── dataframes.py    # Polars DataFrame cleaning
└── tests/
    ├── __init__.py
    ├── test_strings.py
    └── test_dataframes.py
```

## Fun Fact

The name is a nod to the [janitor](https://sfirke.github.io/janitor/index.html) package in R.
