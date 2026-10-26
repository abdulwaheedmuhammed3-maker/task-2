"""Fetch a public repository summary with HTTPX."""

import sys

import httpx


def main():
    repository = sys.argv[1] if len(sys.argv) == 2 else "psf/requests"
    url = f"https://api.github.com/repos/{repository}"
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as error:
        print(f"Could not fetch repository information: {error}", file=sys.stderr)
        return 1
    except ValueError:
        print("The server returned data that was not valid JSON.", file=sys.stderr)
        return 1

    print(f"{data['full_name']}: {data['stargazers_count']} stars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
