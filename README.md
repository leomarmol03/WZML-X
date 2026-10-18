<p align="center">
   <img src="docs/w-icon.svg" alt="WZML-X logo" width="160">
</p>

<h1 align="center">WZML-X</h1>

<p align="center">
   Telegram mirroring and leeching platform with a container-based runtime, a lightweight web UI, and a configurable transfer pipeline.
</p>

<p align="center">
   <a href="https://github.com/SilentDemonSD/WZML-X">
      <img src="https://img.shields.io/github/stars/SilentDemonSD/WZML-X?style=for-the-badge&logo=github&label=Stars" alt="Stars">
   </a>

   <a href="https://github.com/SilentDemonSD/WZML-X/search?l=python">
      <img src="https://img.shields.io/github/languages/top/SilentDemonSD/WZML-X?style=for-the-badge&logo=python&label=Python" alt="Python">
   </a>

   <a href="https://github.com/SilentDemonSD/WZML-X/blob/main/docker-compose.yml">
      <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose">
   </a>

   <a href="https://t.me/WZML_X">
      <img src="https://img.shields.io/badge/Telegram-Community-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
   </a>

   <a href="https://github.com/SilentDemonSD/WZML-X/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/SilentDemonSD/WZML-X?style=for-the-badge&label=License" alt="License">
   </a>

   <a href="https://github.com/SilentDemonSD/WZML-X/commits/main">
      <img src="https://img.shields.io/github/last-commit/SilentDemonSD/WZML-X?style=for-the-badge&label=Last%20Commit" alt="Last Commit">
   </a>
</p>

## Index

<details open>
   <summary>Table of Contents <kbd>Click Here</kbd></summary>

   - [At a Glance](#at-a-glance)
   - [Why Use It](#why-use-it)
   - [What It Covers](#what-it-covers)
   - [How It Runs](#how-it-runs)
   - [Deployment](#deployment)
   - [Google Colab](#google-colab)
   - [Configuration](#configuration)
   - [Project Layout](#project-layout)
   - [Documentation](#documentation)
   - [Support](#support)
   - [Credits](#credits)
   - [License](#license)
</details>

## At a Glance

| Area | Details |
|---|---|
| Runtime | Python Telegram bot + web UI |
| Deployment | Docker & Docker Compose (buildx) |
| Required config | `BOT_TOKEN`, `TELEGRAM_API`, `TELEGRAM_HASH`, `OWNER_ID` |
| Persistence | Optional `DATABASE_URL` (MongoDB Atlas recommended) |
| License | [LICENSE](LICENSE) |

## Why Use It

WZML-X is built for users who want a single bot stack that can mirror, leech, manage files, and expose a simple web-based selection flow without stitching together multiple tools. The README focuses on what you need to deploy it quickly, understand the moving parts, and tune the behavior safely.

## What It Covers

| Capability | Outcome |
|---|---|
| Mirroring | Send files to Telegram with a controllable pipeline |
| Leeching | Deliver files in the format you prefer, including document and media workflows |
| File selection UI | Review and select torrent / NZB / upload contents before finalizing |
| Multi-source downloads | Use qBittorrent, Aria2, JDownloader, Mega, NZB, and yt-dlp integrations |
| Storage and upload paths | Push content to Google Drive, Rclone, Mega, and other supported routes |
| Automation | Limit tasks, tune queues, and manage startup updates from one config layer |

## How It Runs

Deploy with Docker and provide the required configuration values. The container takes care of the runtime path, so users only need to build or start the image and set their settings.

<details>
   <summary>What you need <kbd>Click Here</kbd></summary>

   - Docker installed
   - Your Telegram bot token and Telegram API credentials
   - A MongoDB connection string
   - The optional service credentials you want to enable, such as Drive, Rclone, Mega, JDownloader, or SABnzbd
</details>

## Deployment

<details open>
   <summary>VPS / Dedicated Server (Recommended)</summary>

   ```bash
   git clone https://github.com/SilentDemonSD/WZML-X.git
   cd WZML-X
   cp config_sample.py config.py
   # Edit config.py with your values
   docker buildx compose up -d
   ```

   The bot runs behind a Cloudflare quick tunnel by default. Check the tunnel URL:

   ```bash
   docker compose logs tunnel
   ```

   You'll see a `https://*.trycloudflare.com` URL — that's your bot's web UI.

   To stop:

   ```bash
   docker buildx compose down
   ```
</details>

<details>
   <summary>VPS with VPN (Gluetun)</summary>

   1. Uncomment the `gluetun` service in `docker-compose.yml`
   2. Fill in your VPN provider credentials
   3. Set `network_mode: "service:gluetun"` on the `app` service
   4. Start:

   ```bash
   docker buildx compose up -d
   ```

   All traffic (including the cloudflared tunnel) routes through the VPN.
</details>

<details>
   <summary>Multi-Instance (Multiple Bots)</summary>

   Each bot needs its own `config.py` and data volumes. Example for a second bot:

   1. Create `config2.py` with different `BOT_TOKEN`, `OWNER_ID`, etc.
   2. Uncomment `app2` and `tunnel2` in `docker-compose.yml`
   3. Edit volume mounts to use `config2.py` and separate data dirs
   4. Start:

   ```bash
   docker buildx compose up -d
   ```

   Each bot gets its own cloudflared tunnel URL. Admin ports (qBittorrent, SABnzbd) are mapped to different host ports (`127.0.0.1:8091`, etc.).
</details>

<details>
   <summary>Single Container (Manual)</summary>

   ```bash
   git clone https://github.com/SilentDemonSD/WZML-X.git
   cd WZML-X
   docker build -t wzmlx .
   docker run -p 8080:8080 wzmlx
   ```
</details>

<details>
   <summary>Deployment Notes</summary>

   1. If you use qBittorrent, tune `AsyncIOThreadsCount` to your machine size.
   2. Stop the container before removing it, and remove the container before pruning images.
   3. Useful cleanup commands:

   ```bash
   docker container prune
   docker image prune -a
   ```
</details>

## Google Colab

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/leomarmol03/WZML-X/blob/wzv3/colab/WZML-X-Colab.ipynb)

> [!WARNING]
> Colab runtimes are temporary and can disconnect without notice. They are not suitable for a 24/7 or production bot. Use a VPS or Docker deployment for continuous availability.

Open the ready-to-run [WZML-X Colab notebook](colab/WZML-X-Colab.ipynb). It installs the Linux/Python dependencies normally supplied by the Docker image, creates a private runtime-only `config.py`, starts the bot directly with `python -m bot`, and can create a temporary Cloudflare Quick Tunnel for the file-selector UI.

The notebook defaults to enabling aria2/qBittorrent, disabling JDownloader/SABnzbd, and limiting the bot to two concurrent tasks to stay within Colab's resource limits. It prompts for Telegram credentials without echoing them; `DATABASE_URL` is optional but recommended if settings should persist between sessions. Downloads and other local files are temporary, and the bot clears its download directory on startup. Do not point `WZML_DOWNLOAD_DIR` at persistent storage unless that cleanup behavior is acceptable.

The MEGA integration needs a compatible native C++ SDK Python binding provided by the Docker base image, not by `requirements.txt` or the similarly named PyPI clients. If that binding is missing or incompatible, the bot now starts with MEGA disabled and reports this clearly when a MEGA task is attempted; other download/upload paths remain available. Colab's MEGA support has not been verified.

**Do not run `start.sh` in Colab.** That container-oriented entrypoint invokes `update.py`, which may update or clean deployment files and expects the Docker runtime tooling. The notebook bypasses it. The Cloudflare URL is public and expires with the runtime; stop the tunnel when finished and do not expose private credentials in notebook cells or outputs.

For setup details and troubleshooting, see [`colab/README.md`](colab/README.md).

<details>
   <summary>Legacy Workflow Guide</summary>

   Some users still rely on the external workflow path referenced by the previous README:

   - [WZ Deploy workflow guide](https://github.com/SilentDemonSD/WZ-Deploy/tree/main?tab=readme-ov-file#2%EF%B8%8F%E2%83%A3-method-2-github-workflow-guide)

   Keep this only if that workflow still matches your deployment style.
</details>

## Configuration

Start with the required values:

- `BOT_TOKEN`
- `TELEGRAM_API`
- `TELEGRAM_HASH`
- `OWNER_ID`

`DATABASE_URL` is optional for startup, but a MongoDB Atlas connection is recommended to persist bot settings and user data across restarts. Then tune the optional behavior from `config_sample.py`.

<details>
   <summary>Important user-facing settings</summary>

   | Setting | User impact |
   |---|---|
   | `DEFAULT_LANG` | Bot language |
   | `STATUS_LIMIT` | How much status data is shown |
   | `DEFAULT_UPLOAD` | Default upload target |
   | `LEECH_SPLIT_SIZE` | How large leech outputs are split |
   | `QUEUE_ALL`, `QUEUE_DOWNLOAD`, `QUEUE_UPLOAD` | Queue pressure and concurrency |
   | `SHOW_CLOUD_LINK` | Whether cloud links are shown to users |
   | `WEB_PINCODE` | Protects web access to file selection |
</details>

<details>
   <summary>Integrations available in config</summary>

   The sample config also covers:

   - qBittorrent and Aria2-related controls
   - JDownloader login details
   - Mega credentials
   - SABnzbd server definitions
   - Google Drive settings
   - RSS, search, media metadata, and logging controls
</details>

<details>
   <summary>AllDebrid (<code>-ad</code>)</summary>

   Set `ALLDEBRID_API_KEY` (default: empty, feature off) in `config_sample.py`,
   in the environment, or from **Bot Settings → Config Variables → ALLDEBRID_API_KEY**.

   Add `-ad` to a mirror/leech command to route the input through AllDebrid:

   - `/mirror <filehost link> -ad` unlocks premium hosts (1fichier, rapidgator,
     mega, ...) and hands the direct link to the normal downloader.
   - `/leech <magnet> -ad` (or reply to a `.torrent` with `-ad`) uploads the
     torrent to AllDebrid, waits for it to finish there, then downloads every
     file from AllDebrid's CDN — aria2/qBittorrent are bypassed entirely.

   `ALLDEBRID_NO_SEED_TIMEOUT` (default: `180`) caps how many seconds a magnet may
   stall with no seeders and no download progress before the task is aborted.
   Set it to `0` to disable the check and rely on AllDebrid's own dead-torrent
   reporting instead.

   The flag is documented in the mirror help menu under the **AllDebrid** button.
   Without a key the task fails with `ALLDEBRID_API_KEY is not configured`;
   without `-ad` nothing changes. Magnets stop after 3 min with no seeders and
   2 h overall, and are removed from your AllDebrid history if the task fails.
</details>

## Project Layout

| Path | Purpose |
|---|---|
| `bot/` | Bot core, handlers, listeners, and modules |
| `web/` | FastAPI app, templates, and the file selector UI |
| `gen_scripts/` | Setup helpers for sessions, tokens, and drive configuration |
| `plugins/` | Optional bot plugins |
| `colab/` | Google Colab notebook and setup notes |
| `configs/qbittorrent/` | Default qBittorrent configuration |
| `configs/sabnzbd/` | Default SABnzbd configuration |

## Documentation

> [!NOTE]
> This documentation is still being expanded.

- Full guides: `docs/`
- Deployment notes: the docs site linked from the repository at WZ Docs
- Configuration reference: `config_sample.py`

## Support

<details>
   <summary>Join Community</summary>

   - Telegram channel: https://t.me/WZML_X
   - Support group: https://t.me/WZML_Support
</details>

## Credits

WZML-X is a fork of [mirror-leech-telegram-bot](https://github.com/anasty17/mirror-leech-telegram-bot). The base project belongs to [anasty17](https://github.com/anasty17) and upstream contributors.

<details>
   <summary>Bot Authors</summary>

   <table>
      <thead>
         <tr>
            <th>Avatar</th>
            <th>Name</th>
            <th>Role</th>
            <th>Profile</th>
         </tr>
      </thead>
      <tbody>
         <tr>
            <td><img src="https://avatars.githubusercontent.com/u/105407900?v=4" width="72" alt="SilentDemonSD"></td>
            <td>SilentDemonSD</td>
            <td>Author, UI design, and custom features</td>
            <td><a href="https://github.com/SilentDemonSD">GitHub</a></td>
         </tr>
         <tr>
            <td><img src="https://avatars.githubusercontent.com/u/93116400?v=4" width="72" alt="RjRiajul"></td>
            <td>RjRiajul</td>
            <td>Co-author and maintainer</td>
            <td><a href="https://github.com/rjriajul">GitHub</a></td>
         </tr>
         <tr>
            <td><img src="https://avatars.githubusercontent.com/u/113664541?v=4" width="72" alt="CodeWithWeeb"></td>
            <td>CodeWithWeeb</td>
            <td>Feature expansion and wrap-up improvements</td>
            <td><a href="https://github.com/weebzone">GitHub</a></td>
         </tr>
         <tr>
            <td><img src="https://avatars.githubusercontent.com/u/84721324?v=4" width="72" alt="Maverick"></td>
            <td>Maverick</td>
            <td>Co-author and bug testing</td>
            <td><a href="https://github.com/MajnuRangeela">GitHub</a></td>
         </tr>
      </tbody>
   </table>
</details>

## License

This project is distributed under the terms of the repository license. See [LICENSE](LICENSE) for the full text.

