name: Collect NBA Odds

on:
  schedule:
    - cron: '0 */2 * * *'
  workflow_dispatch:

jobs:
  collect:
    runs-on: ubuntu-latest
    permissions: write-all

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests

      - name: Run parser
        run: python .github/scripts/collect_nba_odds.py

      - name: Commit and push
        run: |
          git config user.name "KUKI Bot"
          git config user.email "bot@kuki.com"
          git add data/
          git diff --quiet && git diff --staged --quiet || git commit -m "Auto-update odds"
          git push
