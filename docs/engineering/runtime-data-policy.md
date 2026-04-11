# Runtime data policy

## Allowed durable data

- synthetic fixtures
- derived structural baselines
- sanitized logs
- release manifests and provenance bundles
- manual screenshots that depict local test systems such as `/docs`
  and `/redoc`

## Forbidden repository data

- private reference PDFs or OCR text
- secrets, tokens, credentials, or session cookies
- copyrighted source newspaper assets

## tmp and log handling

- Use `tmp/` only for disposable scratch data.
- Durable evidence, logs, and release artifacts must not live only
  under `tmp/`.
- If an investigation needs logs, keep the redacted result in a
  durable path or uploaded artifact.

## Safe handling rules

- do not commit secrets
- Keep private reference material local-only.
- Prefer synthetic fixtures for tests, examples, and API security
  exercises.
