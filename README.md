# tg-publisher-vk-post-to-wall

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3116/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/dhvcc/tg-publisher-vk-post-to-wall/blob/master/LICENSE)

## Description
I'm a beginner in Python3, so there may be some bugs.

> [!WARNING]
> After launching the bot, you must immediately select the deferred posting interval that you need! If you do not select it, the post you send will be immediately published in the community!

Telegram bot with which you can post posts to your VK group. Posts can be posted directly or via delayed posting. There are 4 options for the delayed publication timer:
- each hour
- every 2 hours
- every 3 hours
- every 4 hours

The bot is written in Python3, using the asynchronous [aiogram](https://github.com/aiogram/aiogram) library and the synchronous [vk_api](https://github.com/python273/vk_api) library. To get started, you need to get a token for the telegram bot from [@BotFather](https://t.me/BotFather), and also get an API key for working with VK (more details [here](https://dev.vk.com/ru/api/access-token/implicit-flow-user))

## Getting started

### Run in Docker
```
git clone https://github.com/Evgeniy-DevOps/tg-publisher-vk-post-to-wall.git
cd tg-publisher-vk-post-to-wall
docker build --rm --no-cache -t tg-publisher-vk-post-to-wall -f Dockerfile .
docker run --rm -d -e TG_TOKEN='YOUR_TG_TOKEN' -e VK_TOKEN='YOUR_VK_API_KEY' -e VK_GROUP='YOUR_VK_ID_GROUP' tg-publisher-vk-post-to-wall
```

## Support
Pull requests are welcome. To make big changes, please open an issue first to discuss the changes

## License
[MIT](./LICENSE)


