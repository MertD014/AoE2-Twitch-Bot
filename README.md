# 🤖 AoE2 Session Bot

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![TwitchIO](https://img.shields.io/badge/made%20with-TwitchIO-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A versatile Twitch chat bot designed for Age of Empires II streamers. It fetches real-time player stats from the `aoe2recs.com` API and includes a persistent, moderator-controlled scorekeeper to track wins and losses during a stream.

This bot is built to be lightweight, stable, and easily extensible.

---

## ✨ Key Features

- 📈 **Stats:** Fetch current Ranked 1v1 and Team Game ELO with the `!elo` command.
- 🏆 **Persistent Scorekeeper:** Track your session's performance with `!score win` and `!score loss`. The score is saved to a file and survives bot restarts.
- 🛡️ **Moderator Controlled:** Critical commands like adding wins/losses and resetting the score are restricted to moderators and the broadcaster.
- ⚙️ **Efficient & Modern:** Uses `aoe2recs.com` API for fast data retrieval and runs API calls in a separate thread to ensure the bot never freezes.

---

| Command        | Aliases    | Description                                 | Permissions |
| -------------- | ---------- | ------------------------------------------- | ----------- |
| `!elo`         | `!rank`    | Fetches your current AoE2 Ranked ELO.       | Everyone    |
| `!score`       |            | Displays the current session score.         | Everyone    |
| `!score win`   | `!score w` | Adds 1 to the win counter.                  | Mods Only   |
| `!score loss`  | `!score l` | Adds 1 to the loss counter.                 | Mods Only   |
| `!score reset` |            | Resets the score to 0 Wins / 0 Losses.      | Mods Only   |
| `!ping`        |            | Checks if the bot is online and responsive. | Everyone    |
| `!discord`     | `!dc`      | Provides a link to your Discord server.     | Everyone    |

## 📸 Demo in Chat

Will be added...

## 🛠️ Getting Started

Follow these instructions to get a copy of the bot up and running on your local machine for development and testing.

### Prerequisites

- VSCode (Recommended)
- Python 3.8 or newer
- Git
- A Twitch account for your bot
- AoE2 account (if you want to use the aoe related features)

### Installation

1.  - Clone this repository.
2.  - Set up environment variables.
3.  - Run main.py
4.  - Contact me if you need any assistance or feature request.

### Contact Info

- Email : mumtazmertdemir@gmail.com
