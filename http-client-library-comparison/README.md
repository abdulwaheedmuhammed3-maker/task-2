# Choosing a Python HTTP client for SwiftServe

**Word count: about 740 (write-up only; code and source list are not counted).**

## The need

For a SwiftServe pilot, a small service may need to ask a web API for information such as a vehicle record or service status. I compared two free Python libraries for the same job: send a GET request to GitHub's public API, check that the request worked, read the JSON, and print the repository name and star count. This is a small stand-in for reading a SwiftServe service record. Both examples accept the same repository name, use a ten-second timeout, and report network or HTTP errors in a short message.

## Size and dependencies

Both tools are installed with one `pip install` command. Requests has four required runtime dependencies in its current project metadata: `certifi`, `charset_normalizer`, `idna`, and `urllib3`. Its optional SOCKS extra adds PySocks. HTTPX requires `certifi`, `httpcore`, `anyio`, and `idna`; the project also offers separate optional extras for HTTP/2, SOCKS, a CLI and compression formats. So their basic installs have the same number of declared dependencies, but HTTPX has more optional pieces when its extra features are needed. Neither is a one-file library, and both already have the supporting pieces needed for certificates and reliable network connections.

## Maintenance and evidence

The repositories show both projects are maintained, though at different scales. Requests' history lists more than 6,400 commits, and its releases page shows version 2.34.2 published on May 14, 2026. Its issue tracker showed 156 open issues when checked on October 26, 2026, including a compatibility report filed in August ([issue 7617](https://github.com/psf/requests/issues/7617)). HTTPX's repository lists more than 1,500 commits and 64 open issues at the time of review; its newest issue list included a report opened in February 2026 ([issue 3782](https://github.com/encode/httpx/issues/3782)). These counts do not tell us whether a bug will be fixed quickly, but the recent releases, changes and issue discussion show current activity.

There is one maintenance difference I would keep in mind: HTTPX's stable package is still marked Beta in its project metadata, while Requests calls itself Production/Stable. A September 2026 HTTPX discussion also asked when a release beyond 0.28.1 might arrive; a maintainer said there was no set timeline and that a 1.0 release was possible. That is not proof HTTPX is unsafe or abandoned. It does mean a team that requires a clear mature-version signal may prefer Requests, while a team choosing HTTPX should check its release notes and compatibility before upgrading.

## Documentation and writing the examples

Requests' Quickstart is welcoming and easy to scan. It shows a GET request, response text, headers and JSON without much setup. It also clearly warns that Requests has no timeout by default and recommends setting one in nearly all production requests. I appreciated that warning because a simple example can otherwise become unsafe when copied into real work.

HTTPX's QuickStart is similarly direct and includes query parameters, JSON, timeouts and exceptions. Its wider documentation is easier to explore when a project grows: separate guides cover clients, asynchronous use and HTTP/2. HTTPX uses a familiar Requests-like style for the basic call, so the example took almost the same amount of code. I found its `Client` context manager a useful nudge toward reusing connections when SwiftServe makes repeated API calls. For one request, however, that extra idea is not needed.

## Recommendation

For a small SwiftServe pilot that makes a few straightforward, synchronous API calls, I would start with Requests. It has the clearest maturity signal, a very approachable first example, and its long-running release history makes it a comfortable default for a small team. I would still set a timeout and call `raise_for_status()`; a successful network connection does not mean the server returned a useful result.

I would choose HTTPX instead if the pilot is likely to make many concurrent requests, needs asynchronous calls, or may need HTTP/2. Those capabilities are available in one library with an API that remains familiar to a Requests user. I would also pick it if its explicit timeout behavior and client reuse fit the project better. Before adopting either one, I would check its current supported Python versions and dependencies against the team's environment. For now, the extra async and HTTP/2 options do not outweigh Requests' maturity for this small, synchronous job.

## Try both examples

Install each option, then run its example with a repository name. The API request needs an internet connection.

```sh
python -m pip install requests
python requests_example.py psf/requests

python -m pip install httpx
python httpx_example.py psf/requests
```

## Sources checked October 26, 2026

- [Requests Quickstart](https://requests.readthedocs.io/en/stable/user/quickstart/) and [installation guide](https://requests.readthedocs.io/en/latest/user/install/)
- [Requests source repository](https://github.com/psf/requests), [project metadata](https://github.com/psf/requests/blob/main/pyproject.toml), [releases](https://github.com/psf/requests/releases), and [issue tracker](https://github.com/psf/requests/issues)
- [HTTPX QuickStart](https://www.python-httpx.org/quickstart/) and [HTTPX source repository](https://github.com/encode/httpx)
- [HTTPX project metadata](https://github.com/encode/httpx/blob/master/pyproject.toml), [changelog](https://github.com/encode/httpx/blob/master/CHANGELOG.md), [issue tracker](https://github.com/encode/httpx/issues), and [release timeline discussion](https://github.com/encode/httpx/discussions/3792)
