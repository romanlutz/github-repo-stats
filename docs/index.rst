Repository-Stats
================

Refreshed daily!

.. bokeh-plot::
    :source-position: none

    from bokeh.plotting import figure, show
    import json
    
    with open('stats.json', 'r') as stats_file:
        stats = json.load(stats_file)

    p = figure(title="Created issues", plot_width=900)

    # sort created_issues by number of created issues in descending order
    sorted_created_issues = sorted(stats['created_issues'].items(), key=lambda x: x[1], reverse=True)
    names, stats = zip(*sorted_created_issues)
    issues_indices = list(range(len(names)))
    p.vbar(issues_indices, top=stats, line_color='green', line_width=7)
    p.xaxis.ticker = issues_indices
    p.xaxis.major_label_overrides = dict(zip(issues_indices, names))
    p.xaxis.major_label_orientation = 0.75
    show(p)


.. bokeh-plot::
    :source-position: none

    from bokeh.plotting import figure, show
    import json
    
    with open('stats.json', 'r') as stats_file:
        stats = json.load(stats_file)

    p = figure(title="Issue comments", plot_width=900)

    # sort issue_comments by number of issue comments in descending order
    sorted_issue_comments = sorted(stats['issue_comments'].items(), key=lambda x: x[1], reverse=True)
    names, stats = zip(*sorted_issue_comments)
    issues_indices = list(range(len(names)))
    p.vbar(issues_indices, top=stats, line_color='green', line_width=7)
    p.xaxis.ticker = issues_indices
    p.xaxis.major_label_overrides = dict(zip(issues_indices, names))
    p.xaxis.major_label_orientation = 0.75
    show(p)


.. bokeh-plot::
    :source-position: none

    from bokeh.plotting import figure, show
    import json
    from collections import OrderedDict
    
    with open('stats.json', 'r') as stats_file:
        stats = json.load(stats_file)

    p = figure(title="Top referrers", plot_width=900)

    # sort top_referrers by number of referrals in descending order
    sorted_referrals = sorted(stats['top_referrers'].items(), key=lambda x: x[1]['count'], reverse=True)
    referrers, stats = zip(*sorted_referrals)
    indices = list(range(len(referrers)))

    # convert list of dicts to dict of lists for stacked bar chart
    stats = OrderedDict(
        unique=[stat_record['uniques'] for stat_record in stats],
        duplicate=[stat_record['count'] - stat_record['uniques'] for stat_record in stats],
        indices=indices)

    p.vbar_stack(['unique', 'duplicate'], x='indices', source=stats,
                 line_width=7, color=["#e84d60", "#718dbf"],
                 legend_label=['unique', 'duplicate'])
    p.xaxis.ticker = indices
    p.xaxis.major_label_overrides = dict(zip(indices, referrers))
    p.xaxis.major_label_orientation = 0.75
    show(p)


.. bokeh-plot::
    :source-position: none

    from bokeh.plotting import figure, show
    import json
    from collections import OrderedDict
    from datetime import datetime
    
    with open('stats.json', 'r') as stats_file:
        stats = json.load(stats_file)

    p = figure(title="Clones traffic", plot_width=900)

    # sort clones_traffic by date
    sorted_clones_traffic = sorted(stats['clones_traffic'].items())
    dates, stats = zip(*sorted_clones_traffic)
    indices = list(range(len(dates)))

    # convert list of dicts to dict of lists for stacked bar chart
    stats = OrderedDict(
        unique=[stat_record['uniques'] for stat_record in stats],
        duplicate=[stat_record['count'] - stat_record['uniques'] for stat_record in stats],
        indices=indices)

    p.vbar_stack(['unique', 'duplicate'], x='indices', source=stats,
                 line_width=7, color=["#e84d60", "#718dbf"],
                 legend_label=['unique', 'duplicate'])
    p.xaxis.ticker = indices
    p.xaxis.major_label_overrides = dict(zip(indices, dates))
    p.xaxis.major_label_orientation = 0.75
    show(p)


.. bokeh-plot::
    :source-position: none

    from bokeh.plotting import figure, show
    import json
    from collections import OrderedDict
    from datetime import datetime
    
    with open('stats.json', 'r') as stats_file:
        stats = json.load(stats_file)

    p = figure(title="Views traffic", plot_width=900)

    # sort views_traffic by date
    sorted_views_traffic = sorted(stats['views_traffic'].items())
    dates, stats = zip(*sorted_views_traffic)
    indices = list(range(len(dates)))

    # convert list of dicts to dict of lists for stacked bar chart
    stats = OrderedDict(
        unique=[stat_record['uniques'] for stat_record in stats],
        duplicate=[stat_record['count'] - stat_record['uniques'] for stat_record in stats],
        indices=indices)

    p.vbar_stack(['unique', 'duplicate'], x='indices', source=stats,
                 line_width=7, color=["#e84d60", "#718dbf"],
                 legend_label=['unique', 'duplicate'])
    p.xaxis.ticker = indices
    p.xaxis.major_label_overrides = dict(zip(indices, dates))
    p.xaxis.major_label_orientation = 0.75
    show(p)

    # "contributors": {"olliethomas": {"2018-05-13 00:00:00": {"additions": 0, "deletions": 0, "commits": 0}
