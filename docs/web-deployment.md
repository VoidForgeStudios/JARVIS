# JARVIS web deployment without Cloudflare

This setup keeps JARVIS on the Windows machine and exposes only an HTTPS reverse proxy.

```text
GitHub Pages /jarvis/
        |
      HTTPS
        v
   Caddy :443
        |
   localhost:8000
        v
   JARVIS FastAPI
        |
   Claude / tools / SQLite memory
```

## Configure JARVIS

Copy `.env.example` to `.env` and set:

- `JARVIS_API_TOKEN` to a long random secret.
- `JARVIS_CORS_ORIGINS` to the exact GitHub Pages origin, e.g. `https://voidforgestudios.github.io`.
- Your real LLM provider/model and API key when ready.

Never commit `.env`.

## Run locally

From the repository root:

```powershell
python -m uvicorn app.text.server:create_app --factory --host 127.0.0.1 --port 8000
```

Keep Uvicorn on `127.0.0.1`. Do not expose port 8000 directly.

## HTTPS with Caddy

Use a DNS hostname you control, such as `jarvis.example.com`, pointing to your public IP. Install Caddy on Windows and use:

```text
jarvis.example.com {
    reverse_proxy 127.0.0.1:8000
}
```

Caddy can obtain and renew the HTTPS certificate automatically. Allow inbound TCP 443 through the Windows firewall and, if required, forward TCP 443 from the router to the Windows machine. Do not forward 8000.

## Configure the GitHub Pages UI

Set the API base before `app.js` loads:

```html
<script>
  window.JARVIS_API_BASE = "https://jarvis.example.com";
</script>
<script src="app.js" defer></script>
```

The UI asks for the API token and stores it only in browser `sessionStorage`; it is not embedded in GitHub Pages source.

## Verify

Open `https://jarvis.example.com/health`. Then open the GitHub Pages `/jarvis/` page, enter the token, and try `system info` or `calculate 12 * 8`.

A `401` means the token is missing or incorrect. A CORS error means `JARVIS_CORS_ORIGINS` does not exactly match the page origin.

## Security requirements

- Use HTTPS for every public request.
- Use a strong random API token.
- Never put the token in GitHub source or URLs.
- Keep JARVIS bound to localhost.
- Expose only TCP 443 publicly.
- Restrict CORS to the exact Pages origin; never use `*` here.
- This design uses direct HTTPS and does not require Cloudflare.
