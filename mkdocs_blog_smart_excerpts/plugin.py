"""
MkDocs Blog Smart Excerpts Plugin

Automatically creates smart excerpts for blog posts by inserting separators
after a specified number of lines while preserving full content.
"""

import re
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page


class BlogSmartExcerptsConfig(config_options.Config):
    """Configuration options for the blog smart excerpts plugin."""

    max_lines = config_options.Type(int, default=10)
    separator = config_options.Type(str, default="<!-- more -->")
    enable_truncation = config_options.Type(bool, default=True)


class BlogSmartExcerptsPlugin(BasePlugin[BlogSmartExcerptsConfig]):
    """Plugin to automatically create smart excerpts for blog posts."""

    def on_page_markdown(self, markdown, page, config, files):
        """Process page markdown before conversion to HTML."""

        # Only process blog posts (pages in posts directory)
        if not self._is_blog_post(page):
            return markdown

        if not self.config.enable_truncation:
            return markdown

        return self._insert_excerpt_separator(markdown)

    def _is_blog_post(self, page):
        """Check if the page is a blog post."""
        if not page.file:
            return False

        # Check if the page is in the posts directory
        src_path = str(page.file.src_path)
        return "posts/" in src_path and src_path.endswith(".md")

    def _insert_excerpt_separator(self, markdown):
        """Insert separator after specified number of lines at paragraph boundaries."""

        separator = self.config.separator

        # If separator already exists, don't modify
        if separator in markdown:
            return markdown

        # Split markdown into lines
        lines = markdown.split("\n")
        max_lines = self.config.max_lines

        content_lines = []
        non_empty_count = 0
        in_frontmatter = False
        separator_inserted = False
        should_insert_separator = False

        for i, line in enumerate(lines):
            # Handle frontmatter
            if line.strip() == "---":
                in_frontmatter = not in_frontmatter
                content_lines.append(line)
                continue

            if in_frontmatter:
                content_lines.append(line)
                continue

            content_lines.append(line)

            # Count non-empty content lines
            stripped = line.strip()
            if (
                stripped
                and not stripped.startswith("#")
                and not stripped.startswith("<!--")
            ):
                non_empty_count += 1

                # Mark that we should insert separator at next paragraph break
                if non_empty_count >= max_lines and not separator_inserted:
                    should_insert_separator = True

            # Insert separator at paragraph boundaries (empty lines or end of content)
            if should_insert_separator and not separator_inserted:
                # Check if this is a good place to insert (empty line or next line is empty/end)
                next_line_empty = (i + 1 >= len(lines) or lines[i + 1].strip() == "")
                current_line_empty = stripped == ""
                
                if current_line_empty or next_line_empty:
                    if not current_line_empty:
                        content_lines.append("")  # Add empty line if current isn't empty
                    content_lines.append(separator)
                    separator_inserted = True
                    # Add remaining content
                    content_lines.extend(lines[i + 1:])
                    break

        # If we didn't insert separator (short content or no good break point), add at end
        if not separator_inserted:
            if content_lines and content_lines[-1].strip() != "":
                content_lines.append("")
            content_lines.append(separator)

        return "\n".join(content_lines)
