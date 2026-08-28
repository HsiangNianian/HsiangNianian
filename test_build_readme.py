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


if __name__ == "__main__":
    unittest.main()
