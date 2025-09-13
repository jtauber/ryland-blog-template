#!/usr/bin/env python

from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Any
from ryland import Ryland
from ryland.helpers import get_context
from ryland.tubes import load, markdown, project, excerpt


# just to allow url_root to be set on command line
parser = ArgumentParser()
parser.add_argument("--url_root", default="/")
url_root = parser.parse_args().url_root


ryland = Ryland(__file__, url_root=url_root)

ryland.clear_output()


PANTRY_DIR = Path(__file__).parent / "pantry"

ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

PAGES_DIR = Path(__file__).parent / "pages"


tags = {}

def collect_tags():
    def inner(ryland: Ryland, context: Dict[str, Any]) -> Dict[str, Any]:
        extra_context = {"tags": []}
        for tag in get_context("frontmatter.tags", [])(context):
            tag_details = tags.setdefault(
                tag,
                {
                    "tag": tag,
                    "url": f"/tag/{tag}/",
                    "pages": [],
                },
            )
            tag_details["pages"].append(
                ryland.process(
                    context,
                    excerpt(),
                    project(["frontmatter", "url", "excerpt"]),
                )
            )
            extra_context["tags"].append(tag_details)

        return {**context, **extra_context}

    return inner


pages = [
    ryland.process(
        load(page_file),
        markdown(frontmatter=True),
        {"url": get_context("frontmatter.url", f"/{page_file.stem}/")},
        collect_tags(),
        {"template_name": get_context("frontmatter.template_name", "page.html")},
    )
    for page_file in sorted(PAGES_DIR.glob("*.md"))
]

for page in ryland.paginated(pages, fields=["url", "frontmatter"]):
    ryland.render(page)


for tag in tags.values():
    ryland.render(tag, {"template_name": "tag.html"})
