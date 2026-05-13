# Issue Turi AI MVP

AI content planning tool for the YouTube channel "이슈털이".

Current scope:
- Static MVP frontend
- HTTP JSON API
- In-memory repository
- Default fake-agent shorts planning pipeline
- Optional OpenAI real mixed pipeline for manual smoke testing

## Requirements

- Python 3.12
- uv

```powershell
uv run --project . python --version
```

## Tests

```powershell
uv run --project . --with pytest pytest -q
```

Automated tests use fake clients only. They must not call real OpenAI APIs or any other external network APIs.

## Fake Mode

Fake mode is the default and does not require an API key.

Run the browser MVP:

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

Open:

```text
http://127.0.0.1:8000
```

Run the demo payload:

```powershell
uv run --project . python main.py
```

## OpenAI / Real Mode

Real mode currently uses real LLM agents for:
- `RealScriptWriterAgent`
- `RealStoryboardAgent`
- `RealSubtitleAgent`
- `RealVisualAssetSuggestionAgent`
- `RealEditingDirectionAgent`

Safety review is still fake:
- `FakeSafetyReviewAgent`

Create a local `.env` from `.env.example` or set PowerShell environment variables:

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
```

Do not commit `.env` or API keys.

Run the server in real mode:

```powershell
uv run --project . --with openai python -m backend.src.presentation.http.server
```

## Manual Real Smoke Test

Use `smoke-real` when you want to run one topic through the real mixed pipeline without starting the server.

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
uv run --project . --with openai python main.py smoke-real --topic "요즘 사람들이 AI 쇼츠 자동화에 관심 가지는 이유"
```

The command prints formatted JSON to stdout only. It does not save files.

`smoke-real` runs only when `ISSUE_TURI_LLM_PROVIDER` is `openai` or `real`.
If the provider is `fake`, it returns a clear message asking you to select `openai` or `real`.
If `OPENAI_API_KEY` is missing, it returns a clear key-missing error without printing the key value.
If `OPENAI_MODEL` is missing, the default model from settings is used.

## Real Mode Troubleshooting

If `smoke-real` fails, check:
- invalid JSON from a real agent
- missing required JSON fields
- unsupported enum values
- unknown `scene_id`
- missing `OPENAI_API_KEY`
- missing OpenAI SDK when running without `--with openai`

The smoke command includes the exception type, message, and a short hint for JSON contract failures.

## Provider Modes

- `ISSUE_TURI_LLM_PROVIDER=fake`: default fake pipeline
- `ISSUE_TURI_LLM_PROVIDER=openai`: real mixed pipeline with fake safety review
- `ISSUE_TURI_LLM_PROVIDER=real`: same as `openai` for now

## Project Rules

See [AGENTS.md](AGENTS.md) for Codex project instructions, architecture rules, testing rules, and MVP scope.
