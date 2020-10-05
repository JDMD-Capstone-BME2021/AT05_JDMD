# Code Guidelines

*Daniil Shuraev – October 4, 2020*

*version 0.1*

[toc]

## Code Architecture

### Interfaces

Your code must be shipped in a package which exposes only the necessary functions and structures. The interface should not include support structures and methods you are using in the background.

For example you have a file `transform.py` which performs certain mathematical transformations. If you have any helper methods which are not relevant in the context of the package, you need to create an interface `interface.py` which imports only the necessary methods & structures.

```python
#  transform.py
def transform_helper():
    #  this is an internal helper method
    pass


def do_transform():
    #  this method uses helper methods
    tmp = transform_helper()
```

```python
#  interface.py
from transform import do_transform
```

### Exceptions

Check your data inputs, if any of them is invalid, try to return from a function without throwing an exception by returning some valid default value, for example `0`, if you are returning an `int`. However, if the result of function can be misinterpreted, *throw an exception*, for example your `sin()` should not return `0.0` on invalid input.

The thrown exception should include reason for termination as well as relevant parameters. For example `wrong argument value: arg1 expected to be non-negative, received -7.14`.

If you are implementing a custom exception class, it should inherit from standard exception class.

### Data Types

It is recommended that your interface interacts through the standard types (or types which can be *considered* standard).

- Python: standard Python types, but prefer `numpy` structures for vector/matrix representation.
- C++: types in `std::` namespace. It is recommended you use STL containers instead of C types.

### Custom Types

If you are using a custom type, it should expose only appropriate elements. Note which members should be private, protected or public. Note which members could be made static.

- Python: prefer properties to fields to expose type members

### Default Arguments

Use default values on secondary arguments whenever appropriate.

```python
def filt(img, filter_type='gaussian')
```

### Python Type Hints

Include type hints whenever you can.

```python
def foo(a: int) -> dict:
```

## Documentation

Your code must be properly documented, especially the parts which are exposed by the interface.

### Method Docstring

1. Summary of functionality
2. Input arguments, their types and constraints (if any)
3. Return value(s) & type(s)
4. Exceptions if **you** are throwing them
5. Bugs

Documentation can also include

- Usage examples
- Possible
- Algorithm description
- Links to webpages

### Readme

Your package should be accompanied by Readme.md file which should include:

- Installation (if required)
- Summary of functionality and members exposed by the interface
- Examples of usage

## Package Requirements

If you package depends on external packages/libraries, you need to include `requirements.txt` file in root of your package where you list required packages/libraries.

## Style Convention

- `snake_case` for file names
- `CamelCase` for classes, structs, enumerations, etc.
- `snake_case` for functions, methods and properties

## Licensing

If you are using third-party packages, note what sort of license they are using – this will determine the choice of licensing. Pay specific attention to any packages which use *GPL* and its derivatives.



