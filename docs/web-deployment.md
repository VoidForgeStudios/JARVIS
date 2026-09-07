# JARVIS web deployment without Cloudflare

This setup keeps the JARVIS process on the Windows machine while exposing only an HTTPS reverse proxy to the internet.

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
   Claude / tools / data
```

## 1. Configure JARVIS

Copy `.env.example` to `.env` and set:

- `JARVIS_API_TOKEN` to a long random secret.
- `JARVIS_CORS_ORIGINS` to the exact GitHub Pages origin, for example `https://voidforgestudios.github.io`.
- Your real LLM provider/model and API key when ready.

Do not commit `.env`.

## 2. Run JARVIS locally

From the repository root:

```powershell
python -m uvicorn app.text.server:create_app --factory --host 127.0.0.1 --port 8000
```

Keep the application bound to `127.0.0.1`; Caddy is the only process that should accept public traffic.

## 3. Put Caddy in front

Install Caddy on the Windows machine and point a DNS hostname you control at your home/public IP. Then use a Caddyfile like:

```text
jarvis.example.com {
    reverse_proxy 127.0.0.1:8000
}
```

Caddy obtains and renews the HTTPS certificate automatically when the hostname is publicly reachable.

Run Caddy with that Caddyfile and allow inbound TCP 443 on the Windows firewall. If your router has NAT/firewall rules, forward TCP 443 to the Windows machine. Do not forward port 8000.

## 4. Configure the GitHub Pages UI

The web UI supports `window.JARVIS_API_BASE`. Set it before `app.js` loads, for example:

```html
<script>
  window.JARVIS_API_BASE = "https://jarvis.example.com";
</script>
<script src="app.js" defer></script>
```

The UI asks for the API token and stores it only in `sessionStorage` for the current browser session. The token is not embedded in the repository.

## 5. Verify

Open:

```text
https://jarvis.example.com/health
```

Then open the GitHub Pages `/jarvis/` page, enter the token, and try:

```text
system info
calculate 12 * 8
```

A `401` means the token is missing or incorrect. A browser CORS error means `JARVIS_CORS_ORIGINS` does not exactly match the page origin.

## Security notes

- HTTPS is required for a public deployment.
- Use a strong, randomly generated API token.
- Never put the token in GitHub Pages source code, query parameters, or committed configuration.
- Keep JARVIS bound to localhost and expose only Caddy on 443.
- Do not expose the development Uvicorn port directly.
- Restrict CORS to the exact Pages origin; do not use `*` for this personal assistant.
- The API token protects the application, but it is still wise to restrict router/firewall exposure to only the required HTTPS port.
