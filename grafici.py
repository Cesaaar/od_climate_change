import pandas as pd
import numpy as np
import os
import plotly.plotly as py
import plotly.graph_objs as go

'''Trend CO2'''
def trend_co2(co2_anno):
    # Create a trace
    trace = go.Scatter(
        x = co2_anno['Anno'],
        y = co2_anno['Media CO2'],
        mode = 'lines+markers',
        name = 'CO2 Trend'
    )
    data = [trace]

    # Edit the layout
    layout = dict(title = 'Trend storico della concentrazione di CO2 in ppm (parti per milione)',
                  yaxis = dict(title = 'CO2 (ppm)')
                  )

    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Fonte: Osservatorio Mauna Loa, Hawaii (NOAA-ESRL)',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))
    layout['annotations'] = annotations

    fig = dict(data=data, layout=layout)

    return fig

'''Trend Temperatura Terrestre'''
def trend_temp(global_temp):
    trace = go.Scatter(
    x = global_temp['Year'],
    y = global_temp['Glob_C'],
    mode = 'lines'
    )
    data = [trace]

    # Edit the layout
    layout = dict(title = 'Trend storico della temperatura terrestre in gradi C°',
                  yaxis = dict(title = 'gradi (C°)'),
                  shapes=[
                      {
                        'type':'line','x0': global_temp[:1].Year.values[0],'y0': global_temp[:1].Glob_C.values[0],
                            'x1': global_temp[-1:].Year.values[0],'y1': global_temp[:1].Glob_C.values[0], 
                        'line': {'color': 'rgb(178,34,34)','width': 2}
                      },
                      {
                        'type':'line','x0': global_temp[:1].Year.values[0],'y0': global_temp[-1:].Glob_C.values[0],
                            'x1': global_temp[-1:].Year.values[0],'y1': global_temp[-1:].Glob_C.values[0], 
                        'line': {'color': 'rgb(178,34,34)','width': 2}
                      }
                ])

    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Fonte: National Aeronautics and Space Administration (NASA)',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False)
                      )
    annotations.append(dict(x=global_temp[-1:].Year.values[0],y=global_temp[:1].Glob_C.values[0],xref='x',yref='y',
                            text=str(global_temp[:1].Year.values[0])+': '+str(global_temp[:1].Glob_C.values[0])+' C°',
                            ax=0,ay=-10)
                       )

    annotations.append(dict(x=global_temp[-1:].Year.values[0],y=global_temp[-1:].Glob_C.values[0],xref='x',yref='y',
                            text=str(global_temp[-1:].Year.values[0])+': '+str(global_temp[-1:].Glob_C.values[0])+' C°',
                            ax=0,ay=-10)
                       )
    layout['annotations'] = annotations

    fig = dict(data=data, layout=layout)

    return fig
    
    
'''% Riduzione Gas Serra'''
def perc_rid(df_all):
    hover_text = []
    for index, row in df_all.iterrows():
        paese = 'Paese: ' + str(row['Name'])
        perc_rid = '% riduzione: '+ '{:.1%}'.format(row['perc_rid']/100)
        gdp = 'PIL: '+ '{:,}'.format(row['GDP'])+'M€'
        pop = 'Popolazione: '+ '{:,}'.format(row['Habitant'])+'k'
        hover_text.append(paese + '<br>' + perc_rid + '<br>' + gdp + '<br>' + pop)
        
    trace0 = go.Scatter(
    x=df_all['GDP'],
    y=df_all['Habitant'],
    mode='markers',
    text = hover_text,
    hoverinfo='text',
    marker=dict(
        color = df_all['perc_rid'],
        colorbar=dict(title='% riduzione'),
        colorscale='Blues',
        size=df_all['perc_rid']
        )
    )

    layout = go.Layout(
        title='% di Riduzione dei Gas Serra rispetto al 1990',
        xaxis=dict(
            title='Prodotto Interno Lordo (PIL) in milioni di €'+'<br>'+'<i>Fonte: Eurostat</i>',
            type='log',
            autorange=True
        ),
        yaxis=dict(
            title='Numero di abitanti in migliaia',
            type='log',
            autorange=True
        )
    )

    data = [trace0]
    fig = go.Figure(data=data, layout=layout)
    
    return fig
    
    
'''% Riduzione Gas Serra - Mappa'''
def perc_rid_map(df_all):
    hover_text = []
    for index, row in df_all.iterrows():
        paese = 'Paese: ' + str(row['Name'])
        perc_rid = '% riduzione: '+ '{:.1%}'.format(row['perc_rid']/100)
        gdp = 'PIL: '+ '{:,}'.format(row['GDP'])+'M€'
        pop = 'Popolazione: '+ '{:,}'.format(row['Habitant'])+'k'
        hover_text.append(paese + '<br>' + perc_rid + '<br>' + gdp + '<br>' + pop)

    data = [go.Choropleth(
        colorscale = 'Blues',
        autocolorscale = False,
        locations = df_all['Name'],
        z = df_all['perc_rid'],
        locationmode = 'country names',
        text = hover_text,
        marker = go.choropleth.Marker(
            line = go.choropleth.marker.Line(
                color = 'rgb(255,255,255)',
                width = 2
            )),
        colorbar = go.choropleth.ColorBar(
            title = "% Riduzione")
    )]

    layout = go.Layout(
        title = 'Mappa % di Riduzione dei Gas Serra rispetto al 1990',
        geo = go.layout.Geo(
            scope = 'europe',
            projection = go.layout.geo.Projection(type = 'natural earth'),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
    )

    fig = go.Figure(data = data, layout = layout)
    
    return fig

'''% Spesa Clima'''
def perc_spesa(df_all):
    hover_text = []
    for index, row in df_all.iterrows():
        paese = 'Paese: ' + str(row['Name'])
        perc_spesa = '% spesa clima: '+ '{:.1%}'.format(row['perc_spesa']/100)
        gdp = 'PIL: '+ '{:,}'.format(row['GDP'])+'M€'
        pop = 'Popolazione: '+ '{:,}'.format(row['Habitant'])+'k'
        hover_text.append(paese + '<br>' + perc_spesa + '<br>' + gdp + '<br>' + pop)

    trace0 = go.Scatter(
        x=df_all['GDP'],
        y=df_all['Habitant'],
        mode='markers',
        text = hover_text,
        hoverinfo='text',
        marker=dict(
            color = df_all['perc_spesa'],
            colorbar=dict(title='% spesa'),
            colorscale='Blues',
            size=df_all['perc_spesa']*100
            )
        )

    layout = go.Layout(
            title='% di Spesa per il Clima rispetto il Totale della Spesa (2016)',
            xaxis=dict(
                title='Prodotto Interno Lordo (PIL) in milioni di €'+'<br>'+'<i>Fonte: Eurostat</i>',
                type='log',
                autorange=True
            ),
            yaxis=dict(
                title='Numero di abitanti in migliaia',
                type='log',
                autorange=True
            )
        )

    data = [trace0]
    fig_spesa = go.Figure(data=data, layout=layout)
    
    return fig_spesa