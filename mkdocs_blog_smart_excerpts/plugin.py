"""
MkDocs Blog Smart Excerpts Plugin

Automatically creates smart excerpts for blog posts by inserting separators
after a specified number of lines while preserving full content.
"""

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class BlogSmartExcerptsConfig(config_options.Config):
    """Configuration options for the blog smart excerpts plugin."""

    max_lines = config_options.Type(int, default=10)
    auto_inject_separator = config_options.Type(bool, default=True)
    use_frontmatter_excerpt = config_options.Type(bool, default=True)
    verbose = config_options.Type(bool, default=False)

    separator = "<!-- more -->"  # Default separator to use in posts


class BlogSmartExcerptsPlugin(BasePlugin[BlogSmartExcerptsConfig]):
    """Plugin to automatically create smart excerpts for blog posts."""

    def _log(self, message):
        """Log a message if verbose mode is enabled."""
        if self.config.verbose:
            print(f"[BlogSmartExcerptsPlugin] {message}")

    def on_page_markdown(self, markdown, page, config, files):
        """Process page markdown before conversion to HTML."""

        # Only process blog posts (pages in posts directory)
        if not self._is_blog_post(page):
            self._log(f"Skipping non-blog page: {getattr(page.file, 'src_path', None)}")
            return markdown

        # If separator already exists, don't modify
        if self.config.separator in markdown:
            return markdown

        # Check for front matter excerpt first
        if (
            self.config.use_frontmatter_excerpt
            and hasattr(page, "meta")
            and page.meta.get("excerpt")
        ):
            self._log(
                f"Inserting frontmatter excerpt for page: {getattr(page.file, 'src_path', None)}"
            )
            return self._insert_frontmatter_excerpt(markdown, page.meta["excerpt"])

        if self.config.auto_inject_separator:
            self._log(
                f"Auto-injecting excerpt separator for page: {getattr(page.file, 'src_path', None)}"
            )
            return self._insert_excerpt_separator(markdown)

        self._log(
            f"No excerpt or separator injected for page: {getattr(page.file, 'src_path', None)}"
        )
        return markdown

    def _is_blog_post(self, page):
        """Check if the page is a blog post."""
        if not page.file:
            return False

        # Check if the page is in the posts directory
        src_path = str(page.file.src_path)
        is_blog = "posts/" in src_path and src_path.endswith(".md")
        self._log(f"Page src_path: {src_path}, is_blog_post: {is_blog}")
        return is_blog

    def _insert_frontmatter_excerpt(self, markdown, excerpt):
        """Insert excerpt from front matter with separator."""
        separator = self.config.separator

        # Split front matter from content
        lines = markdown.split("\n")

        # Look for front matter (first two --- blocks only)
        if lines and lines[0].strip() == "---":
            # Find the closing --- for front matter
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":  # this is the closing front matter
                    # Front matter is lines[0:i+1], content is lines[i+1:]
                    front_matter_lines = lines[0 : i + 1]
                    content_lines = lines[i + 1 :]
                    break
            else:
                # No closing ---, treat as no front matter
                self._log(
                    "No closing --- found for front matter; treating as no front matter."
                )
                front_matter_lines = []
                content_lines = lines
        else:
            # No front matter
            self._log("No front matter detected. Treating everything as content.")
            front_matter_lines = []
            content_lines = lines

        # Reconstruct with front matter + excerpt + separator + remaining content
        result_lines = front_matter_lines + ["", excerpt, "", separator] + content_lines
        return "\n".join(result_lines)

    def _insert_excerpt_separator(self, markdown):
        """Insert separator after specified number of lines at paragraph boundaries."""

        separator = self.config.separator

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
                next_line_empty = i + 1 >= len(lines) or lines[i + 1].strip() == ""
                current_line_empty = stripped == ""

                if current_line_empty or next_line_empty:
                    if not current_line_empty:
                        content_lines.append(
                            ""
                        )  # Add empty line if current isn't empty
                    content_lines.append(separator)
                    separator_inserted = True
                    self._log(
                        f"Inserted separator after {non_empty_count} content lines at line {i}."
                    )
                    # Add remaining content
                    content_lines.extend(lines[i + 1 :])
                    break

        # If we didn't insert separator (short content or no good break point), add at end
        if not separator_inserted:
            if content_lines and content_lines[-1].strip() != "":
                content_lines.append("")
            content_lines.append(separator)
            self._log("Inserted separator at end of content.")

        return "\n".join(content_lines)
