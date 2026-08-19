import os
import pathlib
import re
import time
import urllib.request

import feedparser
import httpx

root = pathlib.Path(__file__).parent.resolve()


TOKEN = os.environ.get("TOKEN", "")

_http = httpx.Client(timeout=30)  # shared client: reuses connections


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        rf"<!-- {marker} starts -->.*<!-- {marker} ends -->", re.DOTALL
    )
    if not inline:
        chunk = f"\n{chunk}\n"
    chunk = f"<!-- {marker} starts -->{chunk}<!-- {marker} ends -->"
    return r.sub(chunk, content)


def gh_get(path, token, params=None):
    """One authenticated REST call with retry-on-throttle; raises on final failure."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com{path}"
    for attempt in range(4):
        try:
            r = _http.get(url, headers=headers, params=params)
        except httpx.HTTPError as exc:
            print(f"  retry {attempt + 1} for {path}: {exc}")
            time.sleep(1.5 * (attempt + 1))
            continue
        if r.status_code < 500 and r.status_code not in (401, 403, 429):
            return r
        time.sleep(1.5 * (attempt + 1))
    r.raise_for_status()
    return r


def parse_feed(url):
    """feedparser without a timeout can hang forever on dead hosts."""
    with urllib.request.urlopen(url, timeout=20) as f:
        return feedparser.parse(f.read())


def fetch_releases(oauth_token):
    """Latest release per repository, via the REST API.

    GraphQL is deliberately avoided: fine-grained PATs cannot talk to it,
    which is exactly how this section silently died for a long time.
    """
    repo_names = {"playing-with-actions"}  # Skip this one
    repos = []

    def collect_repos(path):
        page = 1
        while True:
            nodes = gh_get(path, oauth_token, {"per_page": 100, "page": page}).json()
            if not nodes:
                return
            for repo in nodes:
                if repo["name"] not in repo_names:
                    repo_names.add(repo["name"])
                    repos.append(repo)
            page += 1

    try:
        me = gh_get("/user", oauth_token).json()
    except Exception as exc:
        raise RuntimeError(
            f"token rejected by GitHub ({exc}) — check the TOKEN secret"
        ) from exc
    collect_repos(f"/users/{me['login']}/repos")
    collect_repos("/orgs/retrofor/repos")

    releases = []
    for repo in repos:
        try:
            r = gh_get(f"/repos/{repo['full_name']}/releases", {"per_page": 1})
            nodes = r.json()
            if not nodes:
                continue
            rel = nodes[0]
            total = 1
            m = re.search(r'[?&]page=(\d+)>;\s*rel="last"', r.headers.get("Link", ""))
            if m:
                total = int(m.group(1))
            published = rel.get("published_at") or rel.get("created_at")
            releases.append(
                {
                    "repo": repo["name"],
                    "repo_url": repo["html_url"],
                    "description": repo.get("description"),
                    "release": (rel.get("name") or rel.get("tag_name") or "")
                    .replace(repo["name"], "")
                    .strip(),
                    "published_at": published or "Near Future",
                    "published_day": published.split("T")[0] if published else "Near Future",
                    "url": rel["html_url"],
                    "total_releases": total,
                }
            )
        except Exception as exc:
            print(f"  release fetch failed for {repo['full_name']}: {exc}")
    return releases


# def fetch_tils():
#     sql = """
#         select path, replace(title, '_', '\_') as title, url, topic, slug, created_utc
#         from til order by created_utc desc limit 5
#     """.strip()
#     return httpx.get(
#         "https://til.simonwillison.net/tils.json",
#         params={"sql": sql, "_shape": "array",},
#     ).json()


def fetch_blog_entries():
    entries = parse_feed("https://academic.jyunko.cn/feed.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["id"],
            "published": entry["published"].split("T")[0],
            "summary": entry["summary"],
        }
        for entry in entries
    ]


def fetch_fm_entries():
    entries = parse_feed("https://fm.jyunko.cn/feed.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["id"],
            "published": entry["published"].split("T")[0],
            "categlory": entry["tags"][1]["term"],
        }
        for entry in entries
    ]


def fetch_diary_entries():
    entries = parse_feed("https://diary.jyunko.cn/feed.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["id"] + '.html',
            "published": entry["published"].split("T")[0]
            # "summary": entry["summary"]
        }
        for entry in entries
    ]


def clean_summary(raw, limit=160):
    """Strip HTML and truncate a feed summary to one readable line."""
    import html as _html

    text = _html.unescape(re.sub(r"<[^>]+>", " ", raw or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


if __name__ == "__main__":
    readme = root / "README.md"
    project_releases = root / "releases.md"
    readme_contents = readme.open().read()
    rewritten = readme_contents

    try:
        releases = fetch_releases(TOKEN)
    except Exception as exc:  # bad token / API down -> keep previous content
        print("release fetch failed:", exc)
        releases = []

    if releases:
        releases.sort(key=lambda r: r["published_at"], reverse=True)
        md = "\n".join(
            "- [{repo} {release}]({url}) · {published_day}".format(**release)
            for release in releases[:10]
        )
        rewritten = replace_chunk(rewritten, "recent_releases", md)
    else:
        print("no releases fetched, keeping previous releases section")

    #     Write out full project-releases.md file
    if releases:
        project_releases_md = "\n".join(
            [
                (
                    (
                        "* **[{repo}]({repo_url})**: [{release}]({url}) {total_releases_md} - {published_day}\n"
                        "<br />{description}"
                    ).format(
                        total_releases_md=f'- ([{release["total_releases"]} releases total]({release["repo_url"]}/releases)) '
                        if release["total_releases"] > 1
                        else "",
                        **release,
                    )
                )
                for release in releases
            ]
        )
        project_releases_content = project_releases.open().read()
        project_releases_content = replace_chunk(
            project_releases_content, "recent_releases", project_releases_md
        )
        project_releases_content = replace_chunk(
            project_releases_content, "project_count", str(len(releases)), inline=True
        )
        project_releases_content = replace_chunk(
            project_releases_content,
            "releases_count",
            str(sum(r["total_releases"] for r in releases)),
            inline=True,
        )
        project_releases.open("w").write(project_releases_content)

    #     tils = fetch_tils()
    #     tils_md = "\n\n".join(
    #         [
    #             "[{title}](https://til.simonwillison.net/{topic}/{slug}) - {created_at}".format(
    #                 title=til["title"],
    #                 topic=til["topic"],
    #                 slug=til["slug"],
    #                 created_at=til["created_utc"].split("T")[0],
    #             )
    #             for til in tils
    #         ]
    #     )
    #     rewritten = replace_chunk(rewritten, "tils", tils_md)
    # blog
    try:
        entries = fetch_blog_entries()[:7]
        entries_md = "\n\n".join(
            '<details><summary>{published} <a href="{url}">{title}</a></summary><p>{summary}</p></details>'.format(
                published=entry["published"],
                url=entry["url"],
                title=entry["title"],
                summary=clean_summary(entry["summary"]),
            )
            for entry in entries
        )
        rewritten = replace_chunk(rewritten, "blog", entries_md)
    except Exception as exc:
        print("blog fetch failed:", exc)
    # fm (README currently has no fm markers; kept safe for future use)
    try:
        fm_entries = fetch_fm_entries()[:6]
        fm_entries_md = "\n\n".join(
            [
                '<details><summary>{published} {categlory}</summary><li><a href="{url}">{title}</a></li></details>'.format(
                    **entry
                )
                for entry in fm_entries
            ]
        )
        rewritten = replace_chunk(rewritten, "fm", fm_entries_md)
    except Exception as exc:
        print("fm fetch failed:", exc)
    # diary (README currently has no diary markers; kept safe for future use)
    try:
        diary_entries = fetch_diary_entries()[:5]
        diary_entries_md = "\n\n".join(
            [
                '<details><summary>{published}</summary><li><a href="{url}">{title}</a></li></details>'.format(
                    **entry
                )
                for entry in diary_entries
            ]
        )
        rewritten = replace_chunk(rewritten, "diary", diary_entries_md)
    except Exception as exc:
        print("diary fetch failed:", exc)

    readme.open("w").write(rewritten)
