import plotly.graph_objects as go
import numpy as np

title = '小値賀人口推移グラフ'
labels = '総人口'
colors = 'rgb(49,130,189)'

mode_size = 12
line_size = 2


x_data = [1920, 1925, 1930, 1935, 1940, 1945, 1950, 1955, 1960, 1965, 1970,
        1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020]


y_data = [ 4648, 10110,  9852,  9478,  9144, 10753, 10968, 10912, 10276,
         9126,  7552,  6374,  5684,  5101,  4651,  4238,  3765,  3268,
         2849,  2560,  2291]


fig = go.Figure()
fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='markers+lines',
        line=dict(color=colors, width=line_size),
        connectgaps=True, 
            ))

# endpoints
fig.add_trace(go.Scatter(
        x=[x_data[0]],
        y=[y_data[0]],
        mode='markers',
        marker=dict(color=colors, size=mode_size)
    ))


fig.add_trace(go.Scatter(
            x=[x_data[20]],
            y=[y_data[20]],
            opacity=1,
            marker = dict(
                size = 6,
                color = 'rgb(220,20,60)',
                line_width = 0
            )))

fig.add_trace(go.Scatter(
            x=[x_data[20]],
            y=[y_data[20]],
            opacity=0.8,
            marker = dict(
                size = 8,
                color = 'rgb(220,20,60)',
                line_width = 0
            )))


fig.add_trace(go.Scatter(
            x=[x_data[20]],
            y=[y_data[20]],
            opacity=0.6,
            marker = dict(
                size = 10,
                color = 'rgb(220,20,60)',
                line_width = 0
            )))


fig.add_trace(go.Scatter(
            x=[x_data[20]],
            y=[y_data[20]],
            opacity=0.4,
            marker = dict(
                size = 25,
                color = 'rgb(220,20,60)',
                line_width = 0
            )))

fig.add_trace(go.Scatter(
            x=[x_data[20]],
            y=[y_data[20]],
            opacity=0.2,
            marker = dict(
                size = 35,
                color = 'rgb(220,20,60)',
                line_width = 0
            )))

fig.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=True,
        zeroline=True,
        showline=True,
        showticklabels=True,
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=130,
        r=20,
        t=110,
    ),
    showlegend=False,
    plot_bgcolor='rgb(240,240,240)'
)
colors_2 = ['rgb(239,243,255)','rgb(189,215,231)','rgb(107,174,214)','rgb(33,113,181)']

fig.add_trace(go.Scatter(
            x=[x_data[6]],
            y=[y_data[6]],
            opacity=1,
            marker = dict(
                size = 6,
                color = 'rgb(49,130,189)',
                line_width = 0
            )))
fig.add_trace(go.Scatter(
            x=[x_data[6]],
            y=[y_data[6]],
            name = 'name',
            marker = dict(
                size = 8,
                color = 'rgb(49,130,189)',
                line_width = 0,
            ),
            opacity=0.8
            
            ))
fig.add_trace(go.Scatter(
            x=[x_data[6]],
            y=[y_data[6]],
            opacity=0.6,
            marker = dict(
                size = 10,
                color = 'rgb(49,130,189)',
                line_width = 0
            )))

fig.add_trace(go.Scatter(
            x=[x_data[6]],
            y=[y_data[6]],
            opacity=0.4,
            marker = dict(
                size = 25,
                color = 'rgb(49,130,189)',
                line_width = 0
            )))

fig.add_trace(go.Scatter(
            x=[x_data[6]],
            y=[y_data[6]],
            opacity=0.2,
            marker = dict(
                size = 35,
                color = 'rgb(49,130,189)',
                line_width = 0
            )))
annotations = []

# Title
annotations.append(dict(xref='paper', yref='paper', x=0.2, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='小値賀町人口推移グラフ',
                              font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='小値賀町ホームページ統計情報人口統計データ',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))

annotations.append(dict(xref='paper', x=0.09, y=3900,
                                  xanchor='right', yanchor='middle',
                                  text=' {}'.format(y_data[0]),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))
# labeling the right_side of the plot
annotations.append(dict(xref='paper', x=0.88, y=y_data[17],
                                  xanchor='left', yanchor='middle',
                                  text='<b>{}人'.format(y_data[20]),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))

annotations.append(dict(xref='paper', x=1950, y=8500,
                                  xanchor='left', yanchor='middle',
                                  text='<b>ピーク時{}人'.format(y_data[6]),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))

fig.update_layout(annotations=annotations)

fig.show()