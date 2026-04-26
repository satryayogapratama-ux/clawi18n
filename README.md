# ClawI18n - Internationalization Framework for OpenClaw

Internationalization (i18n) infrastructure for OpenClaw. Adds multi-language support, locale detection, and language switching capabilities.

## Problem

OpenClaw is powerful but English-only. Users in Southeast Asia, China, and other regions lack native language support. ClawI18n bridges this gap with a professional translation framework.

## Supported Languages

Current language support:

| Language | Code | Status | Completion |
|----------|------|--------|------------|
| English | en | Complete | 100% |
| Bahasa Indonesia | id | Complete | 100% |
| Chinese (Simplified) | zh | Partial | ~30% |
| Thai | th | Partial | ~30% |
| Bahasa Melayu | ms | Partial | ~30% |
| Tiếng Việt | vi | Partial | ~30% |

**Want to add your language?** See [CONTRIBUTING.md](CONTRIBUTING.md)

## Installation

1. Clone or copy this directory into your OpenClaw workspace:
   ```bash
   cp -r clawi18n /path/to/openclaw/workspace/
   ```

2. Install (optional Python dependencies - none required for basic use):
   ```bash
   # i18n.py uses only Python standard library
   # No external dependencies needed
   ```

## Quick Start

### Basic Usage

```python
from clawi18n.i18n import I18n

# Initialize
i18n = I18n(locales_dir='./locales', default_locale='en')

# Translate a string
print(i18n.t('memory.search', locale='id'))
# Output: Mencari memori...

# Translate with variables
print(i18n.t('memory.found', locale='id', count=5))
# Output: Ditemukan 5 memori relevan

# List supported languages
print(i18n.get_supported_locales())
# Output: ['en', 'id', 'ms', 'th', 'vi', 'zh']

# Auto-detect language
detected = i18n.detect_locale('Mencari memori dengan cepat')
print(detected)
# Output: id
```

### Module-Level Convenience Functions

```python
from clawi18n.i18n import init, t, detect_locale, get_supported_locales

# Initialize once
init(locales_dir='./locales')

# Use anywhere
message = t('tool.exec', locale='id')
detected = detect_locale(user_input)
languages = get_supported_locales()
```

### Check Translation Completion

```python
i18n = I18n()
stats = i18n.get_completion_stats()

for locale, info in stats.items():
    print(f"{locale}: {info['completion']}% ({info['translated']}/{info['total']})")

# Output:
# en: 100.0% (59/59)
# id: 100.0% (59/59)
# zh: 32.2% (19/59)
# ...
```

## Integration with OpenClaw

### In OpenClaw Skills

```python
# In a skill's SKILL.md or Python code
from clawi18n.i18n import t, detect_locale

# Detect user's language
user_message = get_user_input()
locale = detect_locale(user_message)

# Use detected language for output
if locale:
    message = t('skill.loaded', locale=locale, name='pajak')
else:
    message = t('skill.loaded', name='pajak')  # Falls back to default

return message
```

### In OpenClaw Responses

```python
# Automatic locale detection from user context
user_locale = extract_user_locale(session)  # Your implementation

# Translate all responses
response = {
    'message': t('success', locale=user_locale),
    'data': process_data()
}
```

## Project Structure

```
clawi18n/
├── locales/
│   ├── en.json          # English (base)
│   ├── id.json          # Indonesian (complete)
│   ├── zh.json          # Chinese (partial)
│   ├── th.json          # Thai (partial)
│   ├── ms.json          # Malay (partial)
│   └── vi.json          # Vietnamese (partial)
├── i18n.py              # Translation engine
├── README.md            # This file
├── CONTRIBUTING.md      # How to add new languages
└── LICENSE              # Evaluation License
```

## Translation Files Format

Each locale is a JSON file with key-value pairs:

```json
{
  "heartbeat.ok": "HEARTBEAT_OK",
  "memory.search": "Mencari memori...",
  "memory.found": "Ditemukan {count} memori relevan",
  "session.active": "Sesi aktif",
  "agent.thinking": "Sedang berpikir...",
  ...
}
```

### Key Naming Convention

Keys use dot notation: `category.action`

Examples:
- `heartbeat.*` - System heartbeats
- `memory.*` - Memory operations
- `session.*` - Session management
- `agent.*` - Agent actions
- `tool.*` - Tool operations
- `error.*` - Error messages
- `browser.*` - Browser operations
- `file.*` - File operations
- `message.*` - Messaging
- `status.*` - Status indicators
- `locale.*` - Language selection

### Variable Substitution

Strings can include variables in `{variable_name}` format:

```json
{
  "memory.found": "Ditemukan {count} memori relevan",
  "file.reading": "Membaca berkas: {path}"
}
```

Use with:
```python
i18n.t('memory.found', locale='id', count=10)
i18n.t('file.reading', locale='id', path='/home/user/file.txt')
```

## API Reference

### I18n Class

#### `__init__(locales_dir=None, default_locale='en')`
Initialize the translation engine.

#### `t(key, locale=None, **kwargs) -> str`
Translate a key with optional variable substitution.

#### `load_locale(lang_code) -> bool`
Load a specific locale's translation file.

#### `detect_locale(text) -> str | None`
Auto-detect language from input text.

#### `get_supported_locales() -> List[str]`
Get list of available locale codes.

#### `get_completion_stats() -> Dict[str, Dict[str, int]]`
Get translation completion percentage for each locale.

## Contributing

We welcome translations! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add a new language
- Guidelines for quality translations
- How to complete partial translations
- Testing and submission process

## Examples

### Example 1: Multi-language Output

```python
i18n = I18n()

keys_to_translate = [
    ('heartbeat.ok', {}),
    ('memory.search', {}),
    ('memory.found', {'count': 10}),
    ('error.generic', {})
]

for locale in ['en', 'id', 'zh', 'th']:
    print(f"\n{locale}:")
    for key, vars in keys_to_translate:
        print(f"  {key}: {i18n.t(key, locale=locale, **vars)}")
```

### Example 2: Locale Detection Pipeline

```python
from clawi18n.i18n import detect_locale, t

def respond_to_user(user_input, fallback_locale='en'):
    # Try to detect language
    detected = detect_locale(user_input)
    target_locale = detected or fallback_locale
    
    # Process and respond in user's language
    result = process(user_input)
    
    return {
        'message': t('success', locale=target_locale),
        'result': result,
        'language': target_locale
    }
```

## License

Evaluation License. See [LICENSE](LICENSE) file.

## Roadmap

- [ ] Complete translations for all partial languages
- [ ] Add contextual pluralization
- [ ] Date/time formatting per locale
- [ ] Currency conversion helpers
- [ ] RTL language support (Arabic, Hebrew)
- [ ] Web UI for translation management
- [ ] Community translation platform integration

## Support

- Issues: GitHub Issues
- Translations: Pull Requests
- Questions: GitHub Discussions

---

**Built for OpenClaw. Made for the world.**
