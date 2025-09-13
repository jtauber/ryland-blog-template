#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Any
from ryland import Ryland
from ryland.helpers import get_context
from ryland.tubes import load, markdown, project, excerpt


# just to allow url_root to be set on command line
parser = ArgumentParser()
parser.add_argument("--url-root", default="/")
url_root = parser.parse_args().url_root


ryland = Ryland(__file__, url_root=url_root)

ryland.clear_output()

PANTRY_DIR = Path(__file__).parent / "pantry"

ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

POSTS_DIR = Path(__file__).parent / "posts"
PAGES_DIR = Path(__file__).parent / "pages"

SITE_DATA = {
    "title": "Ryland Blog Template",
    "description": "a template for a blog built using Ryland",  # optional
    "feed_url": "/atom.xml",
    "author": "James Tauber",
    "host": "https://jtauber.github.io",  # without url-root
}


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
                    "posts": [],
                },
            )
            tag_details["posts"].append(
                ryland.process(
                    context,
                    excerpt(),
                    project(["frontmatter", "url", "excerpt"]),
                )
            )
            extra_context["tags"].append(tag_details)

        return {**context, **extra_context}

    return inner


def calc_url():
    def inner(_: Ryland, context: Dict[str, Any]) -> Dict[str, Any]:
        date = get_context("frontmatter.date")(context)
        title = get_context("frontmatter.title")(context)
        slug = title.lower().replace(" ", "-")
        if date:
            url = f"/{date:%Y}/{date:%m}/{date:%d}/{slug}/"
            return {**context, "url": url}
        else:
            return context

    return inner


for page_file in PAGES_DIR.glob("*.md"):
    ryland.render(
        {"site": SITE_DATA},
        load(page_file),
        markdown(frontmatter=True),
        {"url": get_context("frontmatter.url", f"/{page_file.stem}/")},
        {"template_name": get_context("frontmatter.template_name", "page.html")},
    )

posts = sorted(
    [
        ryland.process(
            load(post_file),
            markdown(frontmatter=True),
            excerpt(),
            collect_tags(),
            calc_url(),
        )
        for post_file in POSTS_DIR.glob("*.md")
    ],
    key=lambda post: post["url"],
    reverse=True,
)

for post in ryland.paginated(posts, fields=["url", "frontmatter"]):
    ryland.render(post, {"template_name": "post.html", "site": SITE_DATA})

for tag in tags.values():
    ryland.render(tag, {"template_name": "tag.html", "site": SITE_DATA})

ryland.render_template("home.html", "index.html", {"posts": posts, "site": SITE_DATA})
ryland.render_template("atom.xml", "atom.xml", {"posts": posts, "site": SITE_DATA, "updated": posts[0]["frontmatter"]["date"]})
