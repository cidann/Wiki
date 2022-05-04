import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def convert(md_data):
    header=(re.findall("(#.+?)\r",md_data))
    anchar=(re.findall("\[.+?]\(.+?\)",md_data))
    list=(re.findall("(\*.+?)\n",md_data))
    bold=(re.findall("(\*\*.+?\*\*)",md_data))
    print(list)
    for h in header:
        md_data=md_data.replace(h,f"<h1>{h[1:]}</h1>")
    for a in anchar:
        linkname=re.split("]\(",a)[0][1:]
        link=re.split("]\(",a)[1][:-1]
        md_data = md_data.replace(a, f"<a href={link}>{linkname}</a>")
    for b in bold:
        md_data=md_data.replace(b,f"<b>{b[2:-2]}</b>")
    if list:
        for l in list:
            if l==list[0]:
                md_data = md_data.replace(l, f"<ul><li>{l[1:]}</li>")
            elif l == list[-1]:
                md_data = md_data.replace(l, f"<li>{l[1:]}</li></ul>")
            else:
                md_data=md_data.replace(l,f"<li>{l[1:]}</li>")
    return md_data


