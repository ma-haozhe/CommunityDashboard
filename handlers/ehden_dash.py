import pandas as pd 
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from . import key_vault, pubmed_miner
import plotly.express as px

def build_ehden_dash():
    results_container=pubmed_miner.init_cosmos('dashboard')
    query="SELECT * FROM c where c.id = 'ehden'"
    items = list(results_container.query_items(query=query, enable_cross_partition_query=True ))
    df=pd.DataFrame(items[0]['data'][4]['course_stats'])
    df2=df[df.user_id!=None].groupby('course_id').max().reset_index()
    df2['course_created']=pd.to_datetime(df2.course_created)
    df2.sort_values('course_created',ascending=False,inplace=True)
    df2['course_fullname']=df2.apply(lambda row:"[{}](https://academy.ehden.eu/course/view.php?id={})".format(row.course_fullname,row.course_id),axis=1)
    df2['completions']=pd.to_numeric(df2.completions)
    df2['started']=pd.to_numeric(df2.started)
    df2.drop(['course_id','user_id','author'],axis=1,inplace=True)

    layout=html.Div([
            dcc.Interval(
                id='interval-component',
                interval=1*1000 # in milliseconds
            ),
            html.Div(
                children=[
                html.Br(),
                html.Br(),
                html.Br(),
                html.H1("Ehden Analysis", 
                    style={
                        'font-family': 'Saira Extra Condensed',
                        'color': '#20425A',
                        'fontWeight': 'bold',
                        'text-align': 'center'
                    }
                ),
                
                html.Div(),
                dash_table.DataTable(
                    id = 'datatable-interactivity',
                    data = df2.to_dict('records'), 
                    columns = [{"name": i, "id": i,'presentation':'markdown'} for i in df2.columns],
                    style_cell={
                        'height': 'auto',
                        # all three widths are needed
                        'minWidth': '10px', 'width': '10px', 'maxWidth': '250px',
                        'whiteSpace': 'normal',
                        'textAlign': 'left'
                    },
                    sort_action='native',
                    page_current=0,
                    page_size=20,
                    page_action='native',
                    filter_action='native',
                    sort_mode="single",         # sort across 'multi' or 'single' columns
                    column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                    selected_columns=[],        # ids of columns that user selects
                    selected_rows=[],           # indices of rows that user selects
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white',
                        'font-family': 'Saira Extra Condensed'
                    },
                    style_filter=[
                        {
                            'color': 'black',
                            'backgroundColor': '#20425A',
                            'font-family': 'Saira Extra Condensed'
                        }
                    ],
                    style_header={
                        'font-family': 'Saira Extra Condensed',
                        'background-color': '#20425A',
                        'color': 'white',
                        'fontWeight': 'bold'
                    }
                )
                        
                ]
            )
        ])
    return layout