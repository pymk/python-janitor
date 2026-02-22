# README

Python string clean-up tool.

## TODO
- [ ] DataFrame: Add DataFrame support

## Examples

```python
normalize_whitespace("hello   world")
# "hello world"

normalize_unicode("café")
# "cafe"

remove_special_characters("hello, world!")
# "hello world"

to_snake_case("hello world")
# "hello_world"

to_kebab_case("hello world")
# "hello-world"

to_pascal_case("hello world")
# "HelloWorld"

to_camel_case("hello world")
# "helloWorld"

clean_string("  héllo   wörld  ")
clean_string("café", unicode=False)
clean_string("hello   world", whitespace=False)
clean_string("hello, world!", special_chars=True)
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
│       ├── dataframes.py    # Polars DataFrame/Series cleaning
│       └── utils.py         # Shared helpers (regex patterns, etc.)
└── tests/
    ├── __init__.py
    ├── test_strings.py
    └── test_dataframes.py
```

## Fun Fact

The name is a nod to the [janitor](https://sfirke.github.io/janitor/index.html) package in R.
