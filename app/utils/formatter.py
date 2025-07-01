from markdown2 import markdown
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def format_llama_response(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(
        r'```(\w+)?\n([\s\S]+?)\n```',
        lambda m: f"\n```{m.group(1) or ''}\n{m.group(2)}\n```\n",
        text
    )
    return markdown(text, extras=["fenced-code-blocks", "tables", "break-on-newline"])