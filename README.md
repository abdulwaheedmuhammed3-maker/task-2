# Global, Crypto & Exchange Suite

## What It Does
A lightweight, mobile-responsive single-page web utility that combines live fiat and cryptocurrency conversion—spanning African regional currencies, global economic powers, and major crypto assets—with a fully functional scientific calculator and quick-access crypto exchange links.

## How to Run It
1. Clone or download the repository containing the `index.html` file.
2. Ensure you have an active internet connection so the script can successfully fetch live exchange rates from the Open Exchange Rates and CoinGecko APIs.
3. Open `index.html` directly in any modern web browser or deploy it via GitHub Pages.

## The One Thing Newcomers Always Get Wrong
New users often assume the application works fully offline, forgetting that it depends on asynchronous API calls to external services (`open.er-api.com` and `coingecko.com`) to load conversion rates on startup. Without an internet connection, the price status will trigger an error message instead of rendering live calculations.
