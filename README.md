# MkDocs Blog Truncate Plugin

A MkDocs plugin that automatically inserts a separator in blog posts after a specified number of lines to create excerpts while preserving the full content for individual post pages.

## Features

- **Inserts separator** (not truncation) - preserves full content while creating excerpts
- **Preserves frontmatter** and handles YAML metadata correctly
- **Smart line counting** - excludes headers, comments, and empty lines
- **Non-destructive** - full content remains available on individual post pages
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
      max_lines: 10          # Number of content lines before separator insertion
      enable_truncation: true # Enable/disable the plugin
```

## Configuration

- `max_lines` (default: 10) - Number of content lines to show before separator insertion
- `enable_truncation` (default: true) - Enable or disable the plugin
- `separator` (default: "<!-- more -->") - The separator used by the blog theme

## How it works

The plugin hooks into the `on_page_markdown` event and:

1. Identifies blog posts in the `posts/` directory
2. Counts content lines (excluding frontmatter, headers, comments)
3. Inserts `<!-- more -->` separator after the specified number of lines
4. **Preserves all remaining content** after the separator
5. Lets the theme's built-in logic handle the "continue reading" functionality

**Important:** This plugin inserts a separator, it does not truncate or remove content. The full post content remains available on individual post pages.

## Requirements

- MkDocs >= 1.0.0
- Material for MkDocs (for blog functionality)

## License

MIT License