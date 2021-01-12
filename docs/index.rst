Repository-Stats
===============

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
    p.vbar(issues_indices, width=1, top=stats)
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
    p.vbar(issues_indices, width=1, top=stats)
    p.xaxis.ticker = issues_indices
    p.xaxis.major_label_overrides = dict(zip(issues_indices, names))
    p.xaxis.major_label_orientation = 0.75
    show(p)


.. bokeh-plot::
    :source-position: none

    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure, show
    import json
    from collections import defaultdict
    from datetime import datetime
    import colorcet as cc
    from numpy import linspace
    
    with open('stats.json', 'r') as stats_file:
        stats = json.load(stats_file)

    # fill the following for customization
    display_at_top = []
    contributors = display_at_top + [name for name in list(stats['contributors'].keys()) if name not in display_at_top]
    contributors = contributors[::-1]
    n_contributors = len(contributors)

    # create more interesting color palette with different color per contributor
    color_palette_step_size = 255 // len(contributors)
    palette = [cc.rainbow[i*color_palette_step_size] for i in range(n_contributors)]

    # determine all time slots - currently by month
    time_slots = set([datetime.strptime(time_slot, '%Y-%m-%d %H:%M:%S')
        for contributor in contributors
        for time_slot in list(stats['contributors'][contributor].keys())])
    time_slots = set([(day.year, day.month) for day in time_slots])
    time_slots = sorted(time_slots, key=lambda day: day[1] + day[0]*12)
    # find min and max and generate time_slots list with all months
    min_year, min_month = time_slots[0]
    max_year, max_month = time_slots[-1]
    time_slots = [(year, month)
        for year in range(min_year, max_year + 1)
        for month in range(1, 13)  # create list of all months in those years, then filter
        if (year > min_year or min_month <= month)  # filter out months that were too early
        and (year < max_year or max_month >= month)]  # filter out months that were too late
    n_months = len(time_slots)

    x = linspace(-1, n_months-1, n_months+1).astype(int)
    source = ColumnDataSource(data=dict(x=x))

    # start at -2 to accommodate a 0 entry in every line
    p = figure(title="Commits", y_range=contributors, plot_width=900, x_range=(-2, n_months+1),
               toolbar_location=None)

    for i, contributor in enumerate(contributors):
        contributor_stats = defaultdict(lambda: defaultdict(int))
        for date_str, date_contrib_stats in stats['contributors'][contributor].items():
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            contributor_stats[date.year][date.month] += date_contrib_stats['commits']
        y = [(contributor, 0)]
        for j in range(len(time_slots)):
            y.append((contributor, contributor_stats[time_slots[j][0]][time_slots[j][1]]))
        source.add(y, contributor)
        p.patch("x", contributor, color=palette[i], alpha=0.6, line_color="black", source=source)

    p.outline_line_color = None
    p.background_fill_color = "#efefef"

    indices = list(range(n_months))
    p.xaxis.ticker = indices
    p.xaxis.major_label_overrides = dict(zip(indices, [f"{slot[1]}/{slot[0]-2000}" for slot in time_slots]))

    p.ygrid.grid_line_color = None
    p.xgrid.grid_line_color = "#dddddd"
    p.xgrid.ticker = p.xaxis.ticker

    p.axis.minor_tick_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.axis_line_color = None

    p.y_range.range_padding = 0.1

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
                 line_width=7, color=["#e84d60", "#718dbf"], width=1,
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
                 line_width=7, color=["#e84d60", "#718dbf"], width=1,
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
                 line_width=7, color=["#e84d60", "#718dbf"], width=1,
                 legend_label=['unique', 'duplicate'])
    p.xaxis.ticker = indices
    p.xaxis.major_label_overrides = dict(zip(indices, dates))
    p.xaxis.major_label_orientation = 0.75
    show(p)
