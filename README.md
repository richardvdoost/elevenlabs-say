# elevenlabs-say

Using elevenlabs.io to improve the `say` command on MacOS.

## Install

Run `make` in the project folder. This will setup a virtual environment in the project
directory under `.venv` and install a `say` command in `/usr/local/bin`.

```bash
make
```

To uninstall:

```bash
make uninstall
```

## Usage

Speak text with the default voice (works with or without quotes):

```bash
say Potatoes are good for me.
say 'Potatoes are good for me.'
```

Get a help message with a list of available voices:

```bash
say -h
```

Speak with a specific voice:
```bash
say -v Charlotte 'I like apples.'
```

Pick a random male or female voice:

```bash
say -v Female 'Are you fast?'
```

```bash
say -v Male 'Last weekend I outran a black pepper snake.'
```

Pick any random voice:

```bash
say -v Any 'I like bacon.'
```

Speak with all available voices (to compare):

```bash
say -v All "Hey it's me."
```


## API Key

If you use this tool without an API key, you have limited usage.

You can fill in your Elevenlabs API key in the `.env` file for more voices and models.

```bash
make env
```
