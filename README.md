# Jeonghan Kim

Personal Jekyll blog for robotics, programming, and theory notes.

This repository now uses the [al-folio](https://github.com/alshedivat/al-folio) v1 theme runtime through Ruby gems, with the existing dated posts preserved under `_posts/`.

## Local build

```bash
bundle install
bundle exec jekyll serve
```

For GitHub Pages, `.github/workflows/deploy.yml` installs the Bundler dependencies, builds the site, uploads `_site` as a Pages artifact, and deploys it with `actions/deploy-pages`. In the repository settings, set Pages to deploy from GitHub Actions, not from the default branch Jekyll builder.

## Academic CV

The `/cv/` page publishes `assets/pdf/academic-cv.pdf`, synced from the sibling Awesome-CV project:

```bash
./scripts/sync-awesome-cv.sh
```
