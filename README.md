# github-repo-stats

Track stats for your repo over time! GitHub tracks certain stats like commits,
additions, deletions, and comments forever. Others like traffic data are only
stored for two weeks. `github-repo-stats` solves this problem by providing a
simple way to track your stats over time.

The key idea here is to periodically run the script in this repo and store the
results. On every run the previous results are updated in order to get a
long-term view at the data.

## How to set up github-repo-stats for your own repo

To avoid having to manually run the script simply set up a new GitHub
repository, configure a GitHub workflow to run the script and use the repo
itself to store the results. Optionally, you can use GitHub Pages to visualize
the results on a custom webpage.

### Setting up a new GitHub repository

Visit the [GitHub website](https://github.com) and click on the plus symbol in
the top right corner next to your profile picture. Select "new repository" and
provide an appropriate name, e.g. "<repo name>-stats". In the following we
assume that you chose "<repo name>-stats", so if you choose something else you
may have to make additional changes.

### Configure the GitHub workflow

In your newly created repository go to "Settings", and then "Secrets". Add a
token with permissions to the repo that you want stats on. To create a
personal access token go to your profile, "Settings", "Developer settings",
"Personal access tokens", and generate a new token. Make the token the least
permissive, i.e., only provide read access. In detail this could mean:

- read:discussion,
- read:enterprise,
- read:org,
- read:packages,
- read:repo_hook,
- read:user,
- repo

We don't use all of these today (yet), but these settings should make your
token future-proof for the purposes of this stats functionality.

Copy your token and store it in your new repo under "Settings", "Secrets" as
"ACCESS_TOKEN". Everyone who has permissions to access the secrets will now
have access to your token, so be careful who you grant access.

Navigate to "Actions" and copy-paste the contents of
`github_workflow_template.yml` from this repository. Replace the values of the
environment variables under `env` near the top of the file with appropriate
ones for your context.

Also copy the files under the `docs` directory into the new repository into
their own `docs` directory. Make sure to substitute the following parts of the
`conf.py` file:

```python
author = '<First Last>'
org = '<org>'  # the org in which you created the stats repo
repo = '<repo>'  # the repository you are tracking
```

In the `index.rst` you can replace the title from `Repository-Stats` to
whatever you find appropriate.

Lastly, copy over the `requirements.txt` file. Commit all these changes.

By default this will run once a day and perform the following actions:

- use `github-repo-stats` script to pull in stats from GitHub
- merge stats with the existing ones in `stats.json` (GitHub provides certain
  stats only for the last 14 days)
- commit updated `stats.json` back to GitHub
- build webpage with visualizations
- commit webpage files to the `gh-pages` branch of the stats repo resulting
  in a deployment to the webpage at `https://<org>.github.io/<repo>-stats`

For debugging purposes it can sometimes be beneficial to add an additional
trigger on `push` to the stats repo. We recommend this only to experienced
users, though.

### Bonus: add a README

It's usually a good practice to add a README to your repository to explain its
purpose. Refer to the
[fairlearn-stats](https://github.com/romanlutz/fairlearn-stats) repo for an
example.

### Updates - how do I get the latest charts?

You don't automatically get the latest charts, because they're a part of
`index.rst`. Simply copy over the latest version whenever you'd like to
upgrade and it should work automatically.
