# MkDocs Blog Smart Excerpts Plugin

A MkDocs plugin that automatically creates smart excerpts for blog posts by inserting separators into the content. This helps in managing long blog posts by providing a "continue reading" link, enhancing the user experience.

See the [Easier Method: Overriding the Template](#easier-method-overriding-the-template) section at the bottom of this README.

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

# Easier Method: Overriding the Template

Instead of using this plugin to modify markdown content, you can achieve similar results by overriding the MkDocs Material blog template to prioritize frontmatter excerpts.

## Template Override Approach

1. **Create template override directory structure:**
   ```
   your-project/
   ├── mkdocs.yaml
   └── overrides/
       └── partials/
           └── post.html
   ```

2. **Enable custom template directory in `mkdocs.yaml`:**
   ```yaml
   theme:
     name: material
     custom_dir: overrides
   ```

3. **Create `overrides/partials/post.html` with excerpt logic:**
   ```html
   <!-- Post content -->
   <div class="md-post__content md-typeset">
     {% if post.meta.excerpt %}
       <!-- Use custom excerpt from front matter -->
       {{ post.meta.excerpt }}
       
       <!-- Always show continue reading link when using custom excerpt -->
       <nav class="md-post__action">
         <a href="{{ post.url | url }}">
           {{ lang.t("blog.continue") }}
         </a>
       </nav>
     {% else %}
       <!-- Fallback to auto-truncation logic -->
       {% set content_lines = post.content.split('\n') %}
       {% if content_lines|length > 4 %}
         {% set truncated_content = content_lines[:10]|join('\n') %}
         {{ truncated_content }}
         
         <nav class="md-post__action">
           <a href="{{ post.url | url }}">
             {{ lang.t("blog.continue") }}
           </a>
         </nav>
       {% else %}
         {{ post.content }}
         
         {% if post.more %}
           <nav class="md-post__action">
             <a href="{{ post.url | url }}">
               {{ lang.t("blog.continue") }}
             </a>
           </nav>
         {% endif %}
       {% endif %}
     {% endif %}
   </div>
   ```

4. **Add excerpt to your blog post frontmatter:**

Note: This excerpt will also get added to the top of the blog. It is unclean right now.
 
   ```yaml
   ---
   title: My Blog Post
   excerpt: "This is my custom excerpt that will appear on the blog listing."
   ---
   ```

## Benefits of Template Override

- **Simpler**: No plugin installation or complex configuration
- **Direct control**: Excerpt logic lives in your template
- **Flexible**: Easy to customize excerpt display and styling
- **No content modification**: Original markdown remains untouched
- **Performance**: No additional markdown processing

## When to Use Each Approach

- **Use template override** for simple excerpt needs and direct control
- **Use this plugin** for automatic separator injection in markdown content and complex excerpt logic
