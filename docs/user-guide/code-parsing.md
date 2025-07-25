# Code Parsing and Analysis

The Gradio MCP Server Builder uses sophisticated code parsing techniques to
analyze your Python functions and generate appropriate MCP servers.
Understanding how this parsing works helps you write better input files and
troubleshoot any issues.

## Overview of the Parsing Process

The parsing process begins when you provide one or more Python files to the
builder. The tool uses Python's built-in `ast` (Abstract Syntax Tree) module to
parse your code, which provides a structured representation of your Python
source code. This approach is more reliable than text-based parsing because it
understands Python syntax and can handle complex code structures.

The parsing workflow involves several stages: file loading, AST generation,
function extraction, signature analysis, and metadata collection. Each stage
builds upon the previous one to create a complete understanding of your
functions.

## Function Detection and Extraction

The builder identifies functions that should be exposed as MCP tools by looking
for the `@mcp.tool()` decorator. This decorator serves as a marker that tells
the parser "this function should become an MCP tool." The parser scans through
all functions in your input files and extracts only those with this specific
decorator.

During extraction, the parser captures the function's name, docstring, parameter
information, return type annotation, and the function's source code. It also
preserves any imports, constants, or helper functions that your decorated
functions depend on.

## Signature Analysis

Once functions are identified, the parser performs detailed signature analysis
to understand the input and output types. This analysis is crucial for
generating appropriate Gradio interface components and ensuring type safety in
the generated MCP server.

The parser examines type hints for each parameter and the return value. It
supports basic Python types like `str`, `int`, `float`, and `bool`, as well as
complex types from the `typing` module such as `List`, `Dict`, `Optional`, and
`Union`. Custom types that can be serialized to JSON are also supported.

For parameters without explicit type hints, the parser attempts to infer types
from default values or docstring annotations. However, explicit type hints are
strongly recommended for the best results.

## Docstring Processing

Docstrings play a crucial role in the parsing process. The parser extracts
docstrings to understand what each function does, what parameters mean, and what
the function returns. This information is used for several purposes:

- Generating better Gradio interface labels and descriptions
- Creating sample prompts for the MCP client
- Improving function documentation in the generated server
- Providing context for AI-powered docstring improvement

The parser handles various docstring formats, including Google-style,
NumPy-style, and plain text docstrings. It extracts parameter descriptions,
return value information, and any examples or usage notes.

## Import and Dependency Analysis

The parser doesn't just look at individual functions; it analyzes the entire
module to understand dependencies and context. It identifies imports that your
functions use, extracts module-level constants and variables, and preserves
helper functions that your decorated functions might call.

This comprehensive analysis ensures that the generated server includes all
necessary imports and dependencies. The parser creates a complete picture of
what your functions need to run properly, including standard library imports,
third-party packages, and local module imports.

## Code Structure Preservation

One of the key features of the parser is its ability to preserve the structure
and organization of your original code. It maintains the order of functions,
preserves comments and formatting where possible, and keeps the logical flow of
your code intact.

This preservation is important because it helps maintain code readability and
makes the generated server easier to understand and modify. The parser also
handles edge cases like nested functions, class methods, and complex control
structures.

## Error Handling and Validation

The parser includes robust error handling to provide helpful feedback when it
encounters issues. It validates function signatures, checks for common problems
like missing decorators or invalid type hints, and provides specific error
messages to help you fix issues.

Common validation checks include:

- Ensuring all decorated functions have valid Python syntax
- Verifying that type hints are properly formatted
- Checking that docstrings are present and well-formed
- Validating that function names follow Python naming conventions

## Sample Prompt Generation

As part of the parsing process, the builder generates sample prompts for each
function. This feature uses the parsed function information to create natural
language prompts that demonstrate how to use each tool.

The sample prompt generation analyzes the function's purpose (from its name and
docstring), its parameters, and its expected behavior. It then creates prompts
that show realistic use cases for the function. These prompts are included in
the generated MCP client and help users understand how to interact with your
tools.

For example, a function named `calculate_area` with parameters `radius` and
`units` might generate prompts like "Calculate the area of a circle with radius
5 meters" or "What's the area of a circle with radius 10 centimeters?"

## Advanced Parsing Features

The parser supports several advanced features that make it more powerful and
flexible:

**Multiple File Processing**: The parser can handle multiple input files
simultaneously, combining functions from different modules into a single MCP
server. This allows you to organize your functions across multiple files while
still generating a unified server.

**Conditional Compilation**: The parser respects Python's conditional
compilation directives and only processes code that would be executed in the
current environment.

**Dynamic Analysis**: For complex functions, the parser can perform dynamic
analysis to better understand parameter types and function behavior.

**Custom Decorators**: While the parser specifically looks for `@mcp.tool()`, it
can be extended to support custom decorators or additional metadata.

## Parsing Configuration

The parsing behavior can be customized through various configuration options.
You can control how the parser handles missing type hints, whether it should be
strict about syntax requirements, and how it processes docstrings.

Configuration options include:

- **Strict mode**: Enforces stricter parsing rules and provides more detailed
  error messages
- **Type inference**: Controls how aggressively the parser tries to infer types
  from context
- **Docstring processing**: Configures how docstrings are analyzed and improved
- **Import handling**: Controls which imports are included in the generated
  server

## Troubleshooting Parsing Issues

If you encounter parsing issues, the builder provides detailed error messages
that help you identify and fix problems. Common issues include:

**Missing Decorators**: Functions without the `@mcp.tool()` decorator are
ignored. Make sure all functions you want to expose have this decorator.

**Invalid Type Hints**: Type hints that can't be parsed or serialized will cause
errors. Use standard Python types or types that can be converted to JSON.

**Syntax Errors**: Python syntax errors in your input files will prevent
parsing. Use a Python linter or IDE to catch syntax issues before running the
builder.

**Import Issues**: Missing or circular imports can cause parsing problems.
Ensure all imports are available and properly organized.

## Performance Considerations

The parsing process is designed to be efficient, but there are some
considerations for large codebases:

**File Size**: Very large files may take longer to parse. Consider breaking
large files into smaller, focused modules.

**Function Count**: Servers with many functions will take longer to generate,
but the parsing itself remains fast.

**Complex Types**: Functions with very complex type hints or nested structures
may require more processing time.

**Dependencies**: Files with many imports or complex dependency graphs may take
longer to analyze.

The parser is optimized for typical use cases and should handle most codebases
efficiently. For very large projects, consider using the `--preserve-docstrings`
flag to skip AI-powered docstring improvement, which can significantly speed up
the build process.
