# Issue Turi AI MVP

AI content planning tool for the YouTube channel "이슈털이".

Current scope:
- Static MVP frontend
- HTTP JSON API
- In-memory repository
- Fake-agent shorts planning pipeline
- Optional real ScriptWriter wiring for manual OpenAI smoke tests

## Requirements

- Python 3.12
- uv

Check the active Python version:

```powershell
uv run --project . python --version
```

## Test

```powershell
uv run --project . --with pytest pytest -q
```

Tests must not call real external APIs.

## Run Fake MVP

Fake mode is the default and does not require an API key.

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

Open:

```text
http://127.0.0.1:8000
```

You can also run the demo payload:

```powershell
uv run --project . python main.py
```

## Run Real ScriptWriter Mode

Real mode currently replaces only `ScriptWriterAgent` with `RealScriptWriterAgent`.
Storyboard, visual suggestions, subtitles, editing directions, and safety review still use fake agents.

Create a local `.env` from `.env.example` and set:

```text
ISSUE_TURI_LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-5
```

Do not commit `.env`.

Run with the OpenAI SDK supplied by uv:

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
uv run --project . --with openai python -m backend.src.presentation.http.server
```

If `OPENAI_API_KEY` is missing, the app raises a clear `OPENAI_API_KEY is required for OpenAILLMClient` error.
If the OpenAI SDK is missing and real mode calls the client, the app reports that the `openai` package is not installed.

## LLM Provider Modes

- `ISSUE_TURI_LLM_PROVIDER=fake`: default fake pipeline
- `ISSUE_TURI_LLM_PROVIDER=openai`: real ScriptWriter only, remaining agents fake
- `ISSUE_TURI_LLM_PROVIDER=real`: same as `openai` for now

## Project Rules

See [AGENTS.md](AGENTS.md) for Codex project instructions, architecture rules, testing rules, and MVP scope.
