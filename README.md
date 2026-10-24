# IND AMICUS LEGAL website (auto-updating)

Daily at about 7:00 am IST, GitHub runs `fetch_updates.py`, saves new regulator items to `updates.json`, and your site shows them under "What's new". No action needed after setup.

## One-time setup (about 10 minutes)
1. Create a free account at github.com and a new **public** repository, for example `indamicus-site`.
2. Upload everything in this folder, **including the hidden `.github` folder**. Easiest: unzip, then drag all files and folders into the repository page.
3. Repository **Settings > Actions > General > Workflow permissions**: choose **Read and write permissions**, then Save.
4. Repository **Settings > Pages**: Source = **Deploy from a branch**, Branch = **main**, folder = **/(root)**, Save. Your site goes live at `https://<username>.github.io/indamicus-site/`.
5. **Actions** tab > "Refresh updates daily" > **Run workflow**, to confirm it works. A green tick means success.
6. Optional: connect your own domain under Settings > Pages > Custom domain.

## Check these feed addresses once
Open each URL in `FEEDS` (top of `fetch_updates.py`) in a browser. It should show XML. These were written from memory and could not be tested live. Fix any that fail and add more regulators if they publish feeds. If a feed fails, the site keeps showing earlier items.

## Good to know
- Each item shows the regulator's title, a short excerpt and a link. Check the official text before acting.
- GitHub pauses scheduled jobs in a repository with no activity for 60 days. Daily refresh commits normally keep it active. If updates stop, press "Run workflow".
- MCA, Income Tax and CBIC may not offer feeds. Those items need adding by hand to `updates.json`.

## Photos
See `images/README.md` for the photo file names. Upload JPGs to the `images` folder and they appear automatically.
