import pathlib
import tempfile
import unittest
from unittest import mock

import httpx

import build_readme


class FakeResponse:
    def __init__(self, payload, headers=None):
        self._payload = payload
        self.headers = headers or {}

    def json(self):
        return self._payload


class FetchReleasesTests(unittest.TestCase):
    def test_release_request_receives_token_and_query_parameters(self):
        repo = {
            "name": "example",
            "full_name": "owner/example",
            "html_url": "https://github.com/owner/example",
            "description": "Example repository  ",
        }
        release = {
            "name": "v1.0.0",
            "tag_name": "v1.0.0",
            "published_at": "2026-08-28T00:00:00Z",
            "html_url": "https://github.com/owner/example/releases/tag/v1.0.0",
        }

        def fake_gh_get(path, token, params=None):
            self.assertEqual(token, "test-token")
            if path == "/user/repos":
                self.assertEqual(
                    params["affiliation"],
                    "owner,collaborator",
                )
                return FakeResponse([repo] if params["page"] == 1 else [])
            if path == "/orgs/retrofor/repos":
                return FakeResponse([])
            if path == "/repos/owner/example/releases":
                self.assertEqual(params, {"per_page": 1})
                return FakeResponse([release])
            self.fail(f"unexpected GitHub API path: {path}")

        with mock.patch.object(build_readme, "gh_get", side_effect=fake_gh_get):
            releases = build_readme.fetch_releases("test-token")

        self.assertEqual(releases[0]["release"], "v1.0.0")
        self.assertEqual(releases[0]["description"], "Example repository")

    def test_all_failed_release_requests_fail_the_build(self):
        repo = {
            "name": "example",
            "full_name": "owner/example",
            "html_url": "https://github.com/owner/example",
            "description": "Example repository",
        }

        def fake_gh_get(path, token, params=None):
            if path == "/user/repos":
                return FakeResponse([repo] if params["page"] == 1 else [])
            if path == "/orgs/retrofor/repos":
                return FakeResponse([])
            if path == "/repos/owner/example/releases":
                raise httpx.HTTPError("GitHub API unavailable")
            self.fail(f"unexpected GitHub API path: {path}")

        with (
            mock.patch.object(build_readme, "gh_get", side_effect=fake_gh_get),
            self.assertRaisesRegex(RuntimeError, "release requests failed"),
        ):
            build_readme.fetch_releases("test-token")


class GitHubRequestTests(unittest.TestCase):
    def test_authentication_failure_is_not_retried(self):
        response = httpx.Response(
            401,
            request=httpx.Request("GET", "https://api.github.com/user"),
        )
        client = mock.Mock()
        client.get.return_value = response

        with (
            mock.patch.object(build_readme, "_http", client),
            mock.patch.object(build_readme.time, "sleep") as sleep,
            self.assertRaises(httpx.HTTPStatusError),
        ):
            build_readme.gh_get("/user", "bad-token")

        client.get.assert_called_once()
        sleep.assert_not_called()


class BlogFeedTests(unittest.TestCase):
    def test_blog_entries_use_the_canonical_feed_link(self):
        feed = {
            "entries": [
                {
                    "title": "Post",
                    "id": "https://academic.jyunko.cn/2026/08/28/Post",
                    "link": "https://academic.jyunko.cn/2026/08/28/Post.html",
                    "published": "2026-08-28T00:00:00Z",
                    "summary": "Summary",
                }
            ]
        }

        with mock.patch.object(build_readme, "parse_feed", return_value=feed):
            entries = build_readme.fetch_blog_entries()

        self.assertEqual(
            entries[0]["url"],
            "https://academic.jyunko.cn/2026/08/28/Post.html",
        )


class ReleasePageTests(unittest.TestCase):
    def test_descriptions_and_empty_descriptions_keep_separate_list_items(self):
        releases = [
            {
                "repo": name,
                "repo_url": f"https://github.com/owner/{name}",
                "description": description,
                "release": "v1.0.0",
                "published_at": "2026-10-12T00:00:00Z",
                "published_day": "2026-10-12",
                "url": f"https://github.com/owner/{name}/releases/tag/v1.0.0",
                "total_releases": 1,
            }
            for name, description in (
                ("first", "First project"),
                ("empty", ""),
                ("last", "Last project"),
            )
        ]
        marker = "<!-- recent_releases starts -->old<!-- recent_releases ends -->"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "README.md").write_text(marker)
            page = root / "releases.md"
            page.write_text(
                "<!-- releases_count starts -->0<!-- releases_count ends -->\n"
                "<!-- project_count starts -->0<!-- project_count ends -->\n"
                + marker
            )
            with (
                mock.patch.object(build_readme, "root", root),
                mock.patch.object(build_readme, "fetch_releases", return_value=releases),
                mock.patch.object(build_readme, "fetch_blog_entries", return_value=[]),
            ):
                build_readme.main()
            content = page.read_text()

        self.assertNotIn("<br", content)
        self.assertEqual(content.count("\n* **["), 3)
        self.assertIn("\n\n  First project\n\n* **[empty]", content)
        self.assertIn(
            "/empty/releases/tag/v1.0.0)  - 2026-10-12\n\n* **[last]", content
        )
        self.assertIn("\n\n  Last project\n<!-- recent_releases ends -->", content)
        self.assertIn("<!-- releases_count starts -->3<!-- releases_count ends -->", content)
        self.assertIn("<!-- project_count starts -->3<!-- project_count ends -->", content)


if __name__ == "__main__":
    unittest.main()
