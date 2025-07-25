# MkDocs Blog Truncate Plugin

A MkDocs plugin that automatically truncates blog post excerpts after a specified number of lines and ensures a "continue reading" link is always shown.

## Features

- **Auto-truncates** blog posts after configurable number of lines
- **Preserves frontmatter** and handles YAML metadata correctly
- **Smart line counting** - excludes headers, comments, and empty lines
- **No HTML parsing** - works at the Markdown level for better performance
- **Configurable** via `mkdocs.yaml`

## Installation

```bash
pip install mkdocs-blog-truncate
```

## Usage

Add to your `mkdocs.yaml`:

```yaml
plugins:
  - blog  # Material for MkDocs blog plugin
  - blog_truncate:
      max_lines: 10          # Number of content lines before truncation
      enable_truncation: true # Enable/disable the plugin
```

## Configuration

- `max_lines` (default: 10) - Number of content lines to show before truncation
- `enable_truncation` (default: true) - Enable or disable the plugin
- `separator` (default: "<!-- more -->") - The separator used by the blog theme

## How it works

The plugin hooks into the `on_page_markdown` event and:

1. Identifies blog posts in the `posts/` directory
2. Counts content lines (excluding frontmatter, headers, comments)
3. Inserts `<!-- more -->` separator after the specified number of lines
4. Lets the theme's built-in logic handle the "continue reading" functionality

## Requirements

- MkDocs >= 1.0.0
- Material for MkDocs (for blog functionality)

## License

MIT License