# elevenlabs-say

Using elevenlabs.io for a better 'say' command.

## Install

Just run `make`. This will install a `say` command in `/usr/local/bin`.

## Usage

Examples:

Speak text: `say Hello world`.

Get a help message with a list of available voices: `say -h`

Test all available voices: `say -v All 'Hello world.'`

Pick a random male / female voice: `say -v Male 'Hello world.'`.

## API Key

Fill in your Elevenlabs API key in the `.env` file for more voices and models.
