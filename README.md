# MkDocs Blog Smart Excerpts Plugin

A MkDocs plugin that automatically creates smart excerpts for blog posts by inserting separators into the content. This helps in managing long blog posts by providing a "continue reading" link, enhancing the user experience.

## Features

- Inserts `<!-- more -->` separator in posts (markdown files) if an existing separator is not already present.
- This is done based on some rules:
  - If the post has a frontmatter excerpt, it uses that.
  - If not, it counts content lines and inserts the separator after a specified number of lines.
    - Excludes headers, comments, and empty lines
    - Inserts separators at natural break points. Does not split paragraphs / lists
- Configurable via `mkdocs.yaml`

## Installation

This is a very baby plugin, so it is not available on PyPI yet. You can install it directly from the source:

```bash
git clone <source>
cd mkdocs-blog-smart-excerpts-plugin
pip install -e .
```

## Usage

Add to your `mkdocs.yaml`:

The default values are given in the example below.

```yaml
plugins:
  - blog  # Material for MkDocs blog plugin
  - blog_smart_excerpts:
      max_lines: 10                    # Number of content lines before separator insertion
      auto_inject_separator: true      # Automatically inject separator if not present
      use_frontmatter_excerpt: true    # Use frontmatter excerpt if available
      verbose: false                     # Enable verbose logging
```

## Configuration

- `max_lines` (default: 10) - Number of content lines to count before inserting separator
- `auto_inject_separator` (default: true) - Automatically inject separator if not already present
- `use_frontmatter_excerpt` (default: true) - Use frontmatter excerpt field if available
- `verbose` (default: false) - Enable verbose logging for debugging

## How it works

The plugin hooks into the `on_page_markdown` event and:

1. Identifies blog posts in the `posts/` directory
2. Counts content lines (excluding frontmatter, headers, comments)
3. Inserts `<!-- more -->` separator based on the following rules:
   1.  after the specified number of lines at paragraph/list boundaries (whichever is later)
   2.  if the post has a frontmatter excerpt, it injects the excerpt at the top. this mangles the content a bit. (TODO: working on a fix)
4. Lets the theme's built-in logic handle the "continue reading" functionality

## Requirements

- MkDocs >= 1.0.0
- Material for MkDocs (for blog functionality)

## License

MIT License