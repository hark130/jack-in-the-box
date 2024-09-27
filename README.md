# jack-in-the-box
Connecting Jackbox Games to the OpenAI API in Python3

## DETAILS

The current [OpenAi API](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) being used.

### Supported Jackbox Games

* [Dictionarium](https://www.jackboxgames.com/games/dictionarium)
* [Joke Boat](https://www.jackboxgames.com/games/joke-boat)
* [Quiplash 2](https://www.jackboxgames.com/games/quiplash-2-interlashional)
* [Quiplash 3](https://www.jackboxgames.com/games/quiplash-3)

## INSTRUCTIONS

1. Download a release wheel from [releases](https://github.com/hark130/jack-in-the-box/releases)
2. `pip install jitb-X.Y.Z-py3-none-any.whl`
3. [Setup your OpenAI API Key](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key)
4. Start a supported [Jackbox Game](https://www.jackboxgames.com/)
5. Get one human signed in (JITB will not function as the VIP)
6. `jitb --user JITB --room <ROOM_CODE>`
7. Start the game

## USAGE

`jitb --help`
