import argparse
from collections import defaultdict, abc
import github
import json
import logging
import os
import sys


_logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def get_client(token):
    if token is not None:
        _logger.info("Received access token.")
        access_token = token

    else:
        with _LogWrapper("reading access token from local file"):
            with open("access_token", "r") as access_token_file:
                access_token = access_token_file.read()

    return github.Github(access_token)


def write_stats_to_file(file_name, stats):
    with open(file_name, 'w') as stats_file:
        json.dump(stats, stats_file, indent=4)


def read_previous_stats_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as stats_file:
            return json.load(stats_file)

    _logger.warning(f"File {file_name} does not exist.")
    return {}


class _LogWrapper:
    def __init__(self, description):
        self._description = description

    def __enter__(self):
        _logger.info("Starting %s", self._description)

    def __exit__(self, type, value, traceback):  # noqa: A002
        # raise exceptions if any occurred
        if value is not None:
            raise value
        _logger.info("Completed %s", self._description)


def recursive_update(d, u):
    """Copied from https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth"""
    for k, v in u.items():
        if isinstance(v, abc.Mapping):
            d[k] = recursive_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def main(args):
    parser = argparse.ArgumentParser(description="Collect GitHub repo stats")
    parser.add_argument("--org", help="GitHub org", required=True)
    parser.add_argument("--repo", help="GitHub repo", required=True)
    parser.add_argument("--token", help="Access token", required=False)
    parser.add_argument("--file-name", help="Stats file", required=True)
    args = parser.parse_args(args)
    org_name = args.org
    repo_name = args.repo
    token = args.token
    file_name = args.file_name

    with _LogWrapper("setting up GitHub client"):
        client = get_client(token)

    repo = client.get_repo(f"{org_name}/{repo_name}")

    stats = {}

    stats['stars'] = repo.stargazers_count

    with _LogWrapper("collecting issues and associated comments"):
        stats['open_issues'] = len(list(repo.get_issues(state='open')))
        stats['closed_issues'] = len(list(repo.get_issues(state='closed')))

        stats['created_issues'] = defaultdict(int)
        stats['issue_comments'] = defaultdict(int)
        for issue in repo.get_issues(state='all'):
            stats['created_issues'][issue.user.login] += 1

            for issue_comment in issue.get_comments():
                stats['issue_comments'][issue_comment.user.login] += 1

    with _LogWrapper("collecting traffic stats"):
        stats['top_referrers'] = {
            referrer.referrer: {
                'count': referrer.count,
                'uniques': referrer.uniques
            }
            for referrer in repo.get_top_referrers()
        }

        stats['clones_traffic'] = {
            str(clone_record.timestamp): {
                'count': clone_record.count,
                'uniques': clone_record.uniques
            }
            for clone_record in repo.get_clones_traffic()['clones']
        }

        stats['views_traffic'] = {
            str(view_record.timestamp): {
                'count': view_record.count,
                'uniques': view_record.uniques
            }
            for view_record in repo.get_views_traffic()['views']
        }

    with _LogWrapper("collecting contributor stats"):
        stats['contributors'] = {
            contributor.author.login: {
                str(week.w): {
                    "additions": week.a,
                    "deletions": week.d,
                    "commits": week.c
                }
                for week in contributor.weeks
            }
            for contributor in repo.get_stats_contributors()
        }

    with _LogWrapper("collecting pull request stats"):
        stats['pull_requests'] = defaultdict(lambda: defaultdict(int))
        for pull_request in repo.get_pulls(state='all', sort='created', base='master'):
            author = pull_request.user.login
            stats['pull_requests'][author]['created'] += 1

            if pull_request.closed_at is None:
                is_open = True
            else:
                is_open = False

            stats['pull_requests'][author]['open'] += int(is_open)
            stats['pull_requests'][author]['closed'] += 1 - int(is_open)

        stats['pull_request_comments'] = defaultdict(int)
        for comment in repo.get_pulls_comments():
            stats['pull_request_comments'][comment.user.login] += 1

    with _LogWrapper("reading previously recorded stats from file"):
        combined_stats = read_previous_stats_from_file(file_name)

    with _LogWrapper("combining old and new stats"):
        recursive_update(combined_stats, stats)

    with _LogWrapper("writing stats to a file"):
        write_stats_to_file(file_name, combined_stats)


if __name__ == "__main__":
    main(sys.argv[1:])
