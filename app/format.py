from markdown2 import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import re


def format_llama_response(text):
    # Удаляем все HTML-теги
    text = re.sub(r'<[^>]+>', '', text)
    
    # Обработка блоков кода (сохраняем их)
    text = re.sub(
        r'```(\w+)?\n([\s\S]+?)\n```',
        lambda m: f"\n```{m.group(1) or ''}\n{m.group(2)}\n```\n",
        text
    )
    
    # Заменяем маркеры списков
    text = text.replace('<ol>', '').replace('</ol>', '')
    text = text.replace('<ul>', '').replace('</ul>', '')
    text = re.sub(r'<li>(.*?)</li>', r'• \1\n', text)
    
    # Заменяем параграфы на переносы строк
    text = text.replace('<p>', '').replace('</p>', '\n\n')
    
    # Удаляем лишние пробелы и переносы
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    
    return text