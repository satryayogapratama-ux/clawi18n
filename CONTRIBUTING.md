# Contributing to ClawI18n

We welcome translations and improvements! This guide explains how to add a new language to ClawI18n.

## Quick Start

### Adding a New Language

1. **Copy the English template**
   ```bash
   cp locales/en.json locales/xx.json
   ```
   Replace `xx` with your language code (e.g., `fr` for French, `de` for German).

2. **Translate all strings**
   Open `locales/xx.json` and translate each value to your language:
   ```json
   {
     "heartbeat.ok": "YOUR_TRANSLATION_HERE",
     "memory.search": "YOUR_TRANSLATION_HERE",
     ...
   }
   ```

3. **Validate JSON syntax**
   Use a JSON validator to ensure no syntax errors:
   ```bash
   python3 -m json.tool locales/xx.json > /dev/null && echo "Valid!"
   ```

4. **Test your translation**
   ```bash
   python3 i18n.py
   ```
   This will show completion stats and sample translations.

5. **Submit your translation**
   - Create a pull request with your new `locales/xx.json` file
   - Include language name and your name in the commit message

## Guidelines

### Translation Quality

- **Be natural, not literal.** Match the tone and style of the English version
- **Use proper terminology** for your language/region
- **Test context.** Read translations in context (variables, UI layout)
- **Keep consistency.** Use the same terms throughout

### Language Codes

Use standard 2-letter ISO 639-1 codes:
- `en` = English
- `id` = Indonesian (Bahasa Indonesia)
- `zh` = Chinese Simplified
- `th` = Thai
- `ms` = Malay (Bahasa Melayu)
- `vi` = Vietnamese
- `fr` = French
- `de` = German
- `es` = Spanish
- `ja` = Japanese
- `ko` = Korean

### What to Translate

1. **Core UI strings** (required)
   - Buttons and actions (save, cancel, delete)
   - Status messages (loading, success, error)
   - Navigation terms (back, next, view)

2. **OpenClaw-specific strings** (required)
   - Agent messages (thinking, executing, searching)
   - Session/memory terms
   - Tool descriptions
   - Skill loading messages

3. **System messages** (required)
   - Error messages with helpful tone
   - Alerts and warnings
   - Timeouts and network errors

## Completing a Partial Translation

Some languages are partially translated. To complete one:

1. Find missing keys by comparing with English:
   ```bash
   python3 -c "
   import json
   en = json.load(open('locales/en.json'))
   xx = json.load(open('locales/xx.json'))
   missing = set(en.keys()) - set(xx.keys())
   for key in sorted(missing):
       print(f'{key}: {en[key]}')
   "
   ```

2. Translate the missing keys and add to your language file

3. Test and submit a pull request

## Locale Detection

If your language has been added, help improve locale detection by suggesting keywords:

1. Edit `i18n.py` in the `LOCALE_KEYWORDS` dictionary
2. Add 10-15 common words from your language
3. These are used to automatically detect language from user input

Example for a language `xx`:
```python
LOCALE_KEYWORDS = {
    'xx': [
        'common_word_1', 'common_word_2', 'common_word_3',
        'common_word_4', 'common_word_5', ...
    ]
}
```

## Testing Your Translation

Use the i18n module to verify:

```python
from i18n import I18n

i18n = I18n()

# Test a simple translation
print(i18n.t('memory.search', locale='xx'))

# Test with variables
print(i18n.t('memory.found', locale='xx', count=5))

# Check completion
stats = i18n.get_completion_stats()
print(f"Your language: {stats.get('xx', {})}")
```

## Reporting Issues

If you find:
- **Mistranslations** in an existing language
- **Missing strings** in a translation
- **Encoding problems** (special characters)
- **Grammar issues**

Please open an issue on GitHub with:
- Language code and name
- The key that's problematic
- Suggested fix

## Recognition

Contributors are recognized in:
- The project's CONTRIBUTORS file
- GitHub commit history
- Completion stats display

Thank you for helping OpenClaw reach global users!

## Questions?

- Check existing translations for style and tone
- Review the OpenClaw documentation for context
- Ask in GitHub discussions if unclear

Happy translating! 🌍
