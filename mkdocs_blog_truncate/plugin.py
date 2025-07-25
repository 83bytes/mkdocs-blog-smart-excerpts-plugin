"""
MkDocs Blog Truncate Plugin

Automatically truncates blog post excerpts after a specified number of lines
and ensures a "continue reading" link is always shown.
"""

import re
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page


class BlogTruncateConfig(config_options.Config):
    """Configuration options for the blog truncate plugin."""
    
    max_lines = config_options.Type(int, default=10)
    separator = config_options.Type(str, default="<!-- more -->")
    enable_truncation = config_options.Type(bool, default=True)


class BlogTruncatePlugin(BasePlugin[BlogTruncateConfig]):
    """Plugin to automatically truncate blog post content."""
    
    def on_page_markdown(self, markdown, page, config, files):
        """Process page markdown before conversion to HTML."""
        
        # Only process blog posts (pages in posts directory)
        if not self._is_blog_post(page):
            return markdown
            
        if not self.config.enable_truncation:
            return markdown
            
        return self._truncate_markdown(markdown)
    
    def _is_blog_post(self, page):
        """Check if the page is a blog post."""
        if not page.file:
            return False
            
        # Check if the page is in the posts directory
        src_path = str(page.file.src_path)
        return 'posts/' in src_path and src_path.endswith('.md')
    
    def _truncate_markdown(self, markdown):
        """Truncate Markdown content after specified number of lines."""
        
        separator = self.config.separator
        
        # If separator already exists, don't modify
        if separator in markdown:
            return markdown
        
        # Split markdown into lines
        lines = markdown.split('\n')
        max_lines = self.config.max_lines
        
        # Skip empty lines and frontmatter for counting
        content_lines = []
        non_empty_count = 0
        in_frontmatter = False
        
        for line in lines:
            # Handle frontmatter
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                content_lines.append(line)
                continue
            
            if in_frontmatter:
                content_lines.append(line)
                continue
            
            content_lines.append(line)
            
            # Count non-empty content lines
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('<!--'):
                non_empty_count += 1
                
                # If we've hit our limit, insert separator
                if non_empty_count >= max_lines:
                    content_lines.append('')  # Add empty line for readability
                    content_lines.append(separator)
                    break
        
        # If we didn't truncate (short content), still add separator for consistency
        if non_empty_count < max_lines and separator not in '\n'.join(content_lines):
            content_lines.append('')
            content_lines.append(separator)
        
        return '\n'.join(content_lines)