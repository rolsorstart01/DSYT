# DSYT No-Code Website Builder

This repository contains a generator that creates a production-ready DSYT trading simulation website with:

- Frontend dashboards, charts, portfolio views, and leaderboard
- Backend trading logic, market models, and authentication
- Admin panel to publish market-moving sector news
- Config-driven architecture for layout, branding, and market rules

## Generate the website

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python builder/generate.py --config builder/config/default.json --output output/dsyt_site
```

Then run the generated site:

```bash
cd output/dsyt_site
pip install -r requirements.txt
python run.py
```

Visit `http://localhost:5000`.
