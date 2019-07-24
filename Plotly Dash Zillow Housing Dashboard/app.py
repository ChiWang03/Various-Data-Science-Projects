import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd


coef = pd.read_csv('lasso_coefficients.csv', index_col = ['Unnamed: 0'])
coef = coef.sort_values(by = 'Penalized Coefficients', ascending = False)

transaction = pd.read_csv('db1data.csv')


jan = transaction[transaction["yearmonth"] == '2016-01'].groupby('fips').count()["parcelid"].values.tolist()
feb = transaction[transaction["yearmonth"] == '2016-02'].groupby('fips').count()["parcelid"].values.tolist()
march = transaction[transaction["yearmonth"] == '2016-03'].groupby('fips').count()["parcelid"].values.tolist()
april = transaction[transaction["yearmonth"] == '2016-04'].groupby('fips').count()["parcelid"].values.tolist()
may = transaction[transaction["yearmonth"] == '2016-05'].groupby('fips').count()["parcelid"].values.tolist()
june = transaction[transaction["yearmonth"] == '2016-06'].groupby('fips').count()["parcelid"].values.tolist()
july = transaction[transaction["yearmonth"] == '2016-07'].groupby('fips').count()["parcelid"].values.tolist()
aug = transaction[transaction["yearmonth"] == '2016-08'].groupby('fips').count()["parcelid"].values.tolist()
sep = transaction[transaction["yearmonth"] == '2016-09'].groupby('fips').count()["parcelid"].values.tolist()
octo = transaction[transaction["yearmonth"] == '2016-10'].groupby('fips').count()["parcelid"].values.tolist()
nov = transaction[transaction["yearmonth"] == '2016-11'].groupby('fips').count()["parcelid"].values.tolist()
dec = transaction[transaction["yearmonth"] == '2016-12'].groupby('fips').count()["parcelid"].values.tolist()

convert_type={31.0: 'Commercial', 46.0: 'MultiStory Store', 47.0: 'Store/Office',
      246.0: 'Duplex',247.0: 'Triplex',248.0:'Quadruplex', 260.0: 'Residential General',
      261.0: 'Single Family Residential',262.0: 'Rural Residence',263.0: 'Mobile Home',
      264.0: 'Townhouse', 265.0: 'Cluster Home', 266.0: 'Condominium',267.0: 'Cooperative',
      268.0: 'Row House',269.0: 'Planned Unit Development', 270.0: 'Residential Common Area',
      271.0: 'Timeshare', 273.0: 'Bungalow', 274.0: 'Zero Lot Line', 275.0: 'Manufactured/Modular Homes',
      276.0: 'Patio Home', 279.0: 'Inferred Single Family', 290.0: 'Vacant Land',291.0: 'Vacant Land'}

transaction['propertylandusetypeid']=transaction['propertylandusetypeid'].map(convert_type)

LA = transaction[(transaction["fips"] == 6037)]["propertylandusetypeid"].value_counts()  # 6037 = los angeles
orange = transaction[(transaction["fips"] == 6059)]["propertylandusetypeid"].value_counts()  # 6037 = los angeles
ventura = transaction[(transaction["fips"] == 6111)]["propertylandusetypeid"].value_counts()  # 6111 = Ventura County

pcts = [jan,feb,march,april, may,june, july,aug, sep, octo,nov, dec]
l1= []
l2 = []
l3 = []
for i in pcts:
    l1.append(i[0])
    l2.append(i[1])
    l3.append(i[2])


df = pd.read_csv('db2data.csv')
df = df[(df['taxvaluedollarcnt'] <= 10000000) & (df['taxvaluedollarcnt'] >= 250000)]

df['DollarPerSquareFeet'] = df['DollarPerSquareFeet'].round()

mapbox_access_token = ''
map_style = ''

scl = [0, "rgb(0,0,0)"], [0.1, "rgb(0, 0, 128)"], [0.2, "rgb(0, 25, 255)"], \
        [0.3, 'rgb(30,144,255)'], [0.75, "rgb(0, 0, 205)"], [1, "rgb(250, 250, 250)"]

x = ["January", "February", "March","April","May", "June","July","August", "September", "October","November","December"]

app = dash.Dash()
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

df = df.rename(index=str, columns={"DollarPerSquareFeet": "Dollar/m^2", "calculatedfinishedsquarefeet": "Total Square Feet", 'taxvaluedollarcnt':
                              '(Price) Dollars','bedroomcnt':'Bedrooms','roomcnt':'Rooms', 'bathroomcnt':'Bathrooms','garagecarcnt':'Garages','yearbuilt':'Year Built'})

tab2layout = html.Div([dcc.Dropdown(id='my-dropdown',
                               options=[
                                   {'label': 'Dollar Per Square Feet', 'value': 'Dollar/m^2'},
                                   {'label': 'Total Square Feet','value': 'Total Square Feet'},
                                   {'label': 'Price', 'value': '(Price) Dollars'},
                                   {'label': 'Number of Bedrooms', 'value': 'Bedrooms'},
                                   {'label': 'Number of Rooms', 'value': 'Rooms'},
                                   {'label': 'Number of Bathrooms', 'value': 'Bathrooms'},
                                   {'label': 'Number of Garages', 'value': 'Garages'},
                                   {'label': 'Year Built', 'value': 'Year Built'},],
                               value='(Price) Dollars'),
                  dcc.Graph(id='graph-with-dropdown')])



@app.callback(dash.dependencies.Output('graph-with-dropdown', 'figure'),[dash.dependencies.Input('my-dropdown', 'value')])
def update_figure(value):
        trace = []
        trace.append(go.Scattermapbox(lat=df['latitude'],
                                          lon=df['longitude'],
                                          text=df[value].astype(str) + " " + value,
                                          mode='markers',
                                          marker=dict(color=df[value], colorscale=scl, reversescale=True, opacity=0.5,
                                                      size=5,
                                                      colorbar=dict(thickness=10, titleside="right",
                                                                    outlinecolor="rgba(68, 68, 68, 0)",
                                                                    ticks="outside", ticklen=3,
                                                                    showticksuffix="last",
                                                                    ticksuffix=" " + value,
                                                                    dtick= np.round(max(df[value]) / 20)))))
        return {'data': trace, 'layout': go.Layout(autosize=False, width=1350, height=700, hovermode='closest',
                                                       mapbox=dict(accesstoken=mapbox_access_token, bearing=0,
                                                                   center=dict(lat=34, lon=-118.5), style=map_style,
                                                                   pitch=35,
                                                                   zoom=7),
                                                       title='Transaction location by ' + str(value))}

tab1layout = html.Div([
            dcc.Graph(id='Total Number of Transactions by Month and County',
                  figure={'data': [go.Bar(x=x, y=l1, name='Los Angeles',marker={

                                               'showscale': False,
                                               'reversescale': True,
                                               'line': dict(color='rgb(8,48,107)',width=2)}),
                                   go.Bar(x=x, y=l2, name='Orange County',marker={
                                                             'showscale': False,
                                               'reversescale': True,
                                               'line': dict(color='rgb(8,48,107)',width=2)}),
                                   go.Bar(x=x, y=l3, name='Ventura County',marker={
                                               'showscale': False,
                                               'reversescale': True,
                                               'line': dict(color='rgb(8,48,107)',width=2)})],
                          'layout': go.Layout(barmode='stack', title="Number of Transactions by Month")}),
            dcc.Graph(id='Type of Prop',
                figure={'data': [go.Bar(x=LA.index[0:3], y=LA.tolist()[0:3], name='Los Angeles', marker={
                  'showscale': False,
                  'reversescale': True,
                  'line': dict(color='rgb(8,48,107)', width=2)}),
                               go.Bar(x=orange.index[0:2], y=orange.tolist()[0:2], name='Orange County', marker={
                                   'showscale': False,
                                   'reversescale': True,
                                   'line': dict(color='rgb(8,48,107)', width=2)}),
                               go.Bar(x=ventura.index[0:3], y=ventura.tolist()[0:3], name='Ventura County', marker={
                                   'showscale': False,
                                   'reversescale': True,
                                   'line': dict(color='rgb(8,48,107)', width=2)})],
                      'layout': go.Layout(barmode='group', title='Types of Properties by County')}),
             dcc.Dropdown(id='month-dropdown',options=[
                     {'label': 'January', 'value': '2016-01'},
                     {'label': 'February','value': '2016-02'},
                     {'label': 'March', 'value': '2016-03'},
                     {'label': 'April', 'value': '2016-04'},
                     {'label': 'May', 'value': '2016-05'},
                     {'label': 'June', 'value': '2016-06'},
                     {'label': 'July', 'value': '2016-07'},
                     {'label': 'August', 'value': '2016-08'},
                     {'label': 'September', 'value': '2016-09'},
                     {'label': 'October', 'value': '2016-10'},
                     {'label': 'November', 'value': '2016-11'},
                     {'label': 'December', 'value': '2016-12'},],
                          value='2016-01'),
            html.Div(id='graph-month')
])

@app.callback(dash.dependencies.Output('graph-month', 'children'),
    [dash.dependencies.Input('month-dropdown', 'value')])
def update_months(value):
    LA = transaction[(transaction["fips"] == 6037) & (transaction['yearmonth'] == value)]["propertylandusetypeid"].value_counts()  # 6037 = los angeles
    orange = transaction[(transaction["fips"] == 6059) & (transaction['yearmonth'] == value)]["propertylandusetypeid"].value_counts()  # 6037 = los angeles
    ventura = transaction[(transaction["fips"] == 6111) & (transaction['yearmonth'] == value)]["propertylandusetypeid"].value_counts()  # 6111 = Ventura County

    return html.Div([dcc.Graph(id='Graph-month',
              figure={'data': [go.Bar(x=LA.index[0:3], y=LA.tolist()[0:3], name='Los Angeles', marker={
                  'showscale': False,
                  'reversescale': True,
                  'line': dict(color='rgb(8,48,107)', width=2)}),
                               go.Bar(x=orange.index[0:3], y=orange.tolist()[0:3], name='Orange County', marker={
                                   'showscale': False,
                                   'reversescale': True,
                                   'line': dict(color='rgb(8,48,107)', width=2)}),
                               go.Bar(x=ventura.index[0:3], y=ventura.tolist()[0:3], name='Ventura County', marker={
                                   'showscale': False,
                                   'reversescale': True,
                                   'line': dict(color='rgb(8,48,107)', width=2)})],
                      'layout': go.Layout(barmode='group', title='Types of Properties by County')})])


tab4layout = [html.Div([dcc.RangeSlider(id='my-slider',min=-10000,max=90000,step=1000,value=[-10000, 90000],),
                        html.H1(children = ''' LASSO: uses the l1 penalty to force some of the coefficient estimates to be exactly equal to zero when the tuning parameter λ is sufficiently large'''),
                        html.Div(id='graph-with-slider'),
                        html.H3(children='''LASSO may not be the best method to find an accurate model since it assumes a linear relationship and ignores the fact that predictors tend to depend on the coefficients of the other predictors'''),
                        html.H3(children='''However, We just want to demonstrate an easy way of Variable Selection '''),
                        html.H3(children='''LASSO removed quite a few predictors, this can be seen as the coefficients that are penalized to 0.'''),
                        html.H3(children='''Note: this is not really accurate, could be optmized with many different methods!'''),
                        html.H1(children = '''                 '''),
                        html.H3(children='''Fact: measuring importance in some way or other doesn't tell you where to draw the line between "important" & "unimportant".'''),
                        html.H3(children='''The importance of one predictor tends to depend on the coefficients of other predictors in the model'''),
                        html.H3(children=''' e.g. LASSO paths cross, Walds chi-squareds change as predictors are removed. So you could perform variable selection by simply using a cut-off on an importance measure, but most methods are more complex. By Statistics Overflow'''),
                        ])]


@app.callback(dash.dependencies.Output('graph-with-slider', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])

def update_figure1(value):
    vals = coef[(coef['Penalized Coefficients'] >= value[0])  & (coef['Penalized Coefficients'] <= value[1]) ]
    return html.Div([dcc.Graph(id="graphwithslider", figure={'data': [go.Bar(x=[i[0] for i in vals.values], y=vals.index.tolist(), orientation = 'h',text=[i[0] for i in vals.values],
                                           marker={'color': [i[0] for i in coef.values],'colorscale': 'Viridis','showscale': False,'reversescale': True,'line': dict(color='rgb(8,48,107)', width=2)})],
                          'layout': go.Layout(title="Penalized Coefficients")})])



import dash_html_components as html
import base64




test1_png = 'Errorplot1.png'
test1_base64 = base64.b64encode(open(test1_png, 'rb').read()).decode('ascii')
test2_png = 'Errorplot2.png'
test2_base64 = base64.b64encode(open(test2_png, 'rb').read()).decode('ascii')
test3_png = 'Errorplot3.png'
test3_base64 = base64.b64encode(open(test3_png, 'rb').read()).decode('ascii')

tab3layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(test1_base64),style={'width': '1100px'}),
    html.Img(src='data:image/png;base64,{}'.format(test2_base64),style={'width': '1100px'}),
    html.Img(src='data:image/png;base64,{}'.format(test3_base64),style={'width': '1100px'})
    ])





app.layout = html.Div(
   children=[
      dcc.Tabs(
         id='tabs', value=1, children=[
            dcc.Tab(label='Market Volume', value=1),
            dcc.Tab(label='Geolocation by Property Feature', value=2),
            dcc.Tab(label='Error Plots', value=3),
            dcc.Tab(label = 'Predictive Modelling', value = 4),
            ]
      ),
   html.Div(id='tab-output')
   ]
)


import dash_html_components as html
import dash_table


tab5layout = html.Div([
    dash_table.DataTable(
        columns=[{
            'name': 'Column {}'.format(i),
            'id': 'column-{}'.format(i)
        } for i in range(1,15)],
        data=[
            {'column-{}'.format(i): (j + (i-1)*5) for i in range(1, 15)}
            for j in range(5)
        ],
        style_table={'overflowX': 'scroll'},
    )], style={'width':500})


@app.callback(Output('tab-output', 'children'),[Input('tabs', 'value')])

def show_content(value):
    if value == 1:
        return tab1layout
    elif value == 2:
        return tab2layout
    elif value == 3:
        return tab3layout
    elif value == 4:
        return tab4layout




if __name__ == '__main__':
    app.run_server(debug=True, port =9000)
