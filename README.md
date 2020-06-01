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
provide an appropriate name, e.g. "<repo name>-stats".

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
`github_workflow_template.yml` from this repository. Replace all occurrences
of `<org>` with the organization of the repository you want to track, and
`<repo>` with the repository itself.

### Deploy a webpage to GitHub pages and visualize the results

TODO
