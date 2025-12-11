 ChuckBot

A powerful Discord bot developed in Python designed for rapid, administrative actions, including mass channel creation and concurrent message spamming (nuke bot btw)

**Disclaimer:** This bot performs disruptive actions. It should only be used on servers you own or have explicit permission to test on.

## Features

*   **Mass Channel Deletion:** Instantly removes all existing channels from the server
*   **Rapid Channel Creation:** Continuously creates new text channels at high speed
*   **Concurrent Spamming:** Alternates between creating new channels and sending `@everyone` pings to all available channels simultaneously
*   **Optimized Performance:** Uses `asyncio` and `asyncio.gather` to maximize throughput within Discord's API rate limits

## Prerequisites

*   Python 3.8+ installed
*   The `discord.py` library:
    ```bash
    pip install discord.py
    ```

## Installation and Setup

### 1. Get the Code

Clone the repository to your local machine:

```bash
git clone github.com
cd ChuckBot
