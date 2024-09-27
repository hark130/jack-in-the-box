# jack-in-the-box
Jack in the Box (JITB): Connecting Jackbox Games to the OpenAI API in Python3

## DETAILS

JITB uses this [OpenAi API](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) with the [gpt-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini) model to generate content and a [Google Chrome](https://www.google.com/chrome/) browser, by way of [Selenium](https://www.selenium.dev/documentation/webdriver/), to interact with the [Jackbox Games](https://www.jackboxgames.com/).

### Supported Jackbox Games

* [Dictionarium](https://www.jackboxgames.com/games/dictionarium)
* [Joke Boat](https://www.jackboxgames.com/games/joke-boat)
* [Quiplash 2](https://www.jackboxgames.com/games/quiplash-2-interlashional)
* [Quiplash 3](https://www.jackboxgames.com/games/quiplash-3)

## INSTRUCTIONS

1. [Download and install Google Chrome](https://support.google.com/chrome/answer/95346?hl=en-GB&co=GENIE.Platform%3DDesktop)
1. Download a release wheel from [releases](https://github.com/hark130/jack-in-the-box/releases)
1. `pip install jitb-X.Y.Z-py3-none-any.whl`
1. [Setup your OpenAI API Key](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key)
1. Start a supported [Jackbox Game](https://www.jackboxgames.com/)
1. Get one human signed in (JITB will not function as the VIP)
1. `jitb --user JITB --room <ROOM_CODE>`
1. Start the game


## USAGE

`jitb --help`

OPTIONAL: Use the `TMPDIR` environment variable to control the debug log file location.
