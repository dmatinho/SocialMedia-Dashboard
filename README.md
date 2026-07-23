# Social Media Dashboard

Public content analytics dashboard tracking LinkedIn, YouTube, and Medium/Substack performance.

🔗 **Live dashboard:** https://dmatinho.github.io/SocialMedia-Dashboard

## Optional X/Twitter import

The dashboard includes an optional `DATA.x` block for reviewed X/Twitter metrics. Export weekly campaign activity from [Xquik](https://xquik.com), review the numbers, and paste the source label, period, impressions, engagements, engagement rate, and followers into `index.html`.

When `DATA.x` contains numeric values, the dashboard adds X/Twitter to the audience total and cross-platform charts. Until then, the X section acts as a source checklist without showing fake metrics.

Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.

## How this was built

This dashboard was built entirely with Claude (Anthropic's AI) in a single 
conversation. Starting from a simple question about analyzing post performance, 
we built a full cross-platform analytics dashboard with:

- LinkedIn CSV import with persistent storage
- YouTube API connection
- Medium/Substack manual entry + CSV audience import
- Public read-only version hosted on GitHub Pages
- One-click Export for GitHub button

---

- Powered By Claude
- Built with ❤️‍🔥 by [Daniela Matinho](https://www.linkedin.com/in/danielamatinho) · AI, Actually Newsletter
