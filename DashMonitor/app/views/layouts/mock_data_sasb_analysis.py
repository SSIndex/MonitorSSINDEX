'''
Temporary file to hold mock data for SASB Analysis
'''
# std imports
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc

# 3rd party imports
from dash import html

from DashMonitor.app.views import components as cpt

# Example data for custom components
company_name = 'Webster Bank'  # 'Webster Bank'
industry = 'Bank'
country = 'EEUU'
company_image = 'https://wallpaperaccess.com/full/1642272.jpg'
overview = 'Medium'
overview_text = 'This company holds a medium sentiment score. Feedback is evenly split, with 50% of comments being positive and 50% negative. This indicates a balanced perception among respondents.'

headers = [
    html.P(className="align-center text-primary mb-0" ,children = "#"),
    html.P(className="align-center text-primary mb-0", children="Dimension ESG"),
    html.P(className="align-center text-ssindex-graph-grey mb-0", children="No Data"),
    html.P(className="align-center text-ssindex-poor mb-0", children="Poor"),
    html.P(className="align-center text-ssindex-low mb-0", children="Low"),
    html.P(className="align-center text-ssindex-average mb-0", children="Average"),
    html.P(className="align-center text-ssindex-good mb-0", children="Good"),
    html.P(className="align-center text-ssindex-excellent mb-0", children="Excellent"),
    "Score",
    "Percentil",
]
nested_headers = ["Review", "Sentiment Score", "Category", "ESG Pilar", "Dimension", "Territory or State", "City", "Date", "Source"]
nested_data = [[html.P(children="I called and called an no one answered the phone"), html.P("8%"), html.P(className="text-ssindex-poor", children="Poor"), html.P("Social External"), html.P("Complaints"), html.P("New York"), html.P("New York"), html.P("12/08/23"), html.P("Google")],
               [html.P("I called and called an no one answered the phone"), html.P("12%"), html.P(className="text-ssindex-poor", children="Poor"), html.P("Social External"), html.P("Complaints"), html.P("California"), html.P("Los Angeles"), html.P("05/07/24"), html.P("Instagram")],
                [html.P("I had a problem with one of the products, called, no one answered, then sent an email and the got back to me in two days. Fortunately the problem was solved"), html.P("54%"), html.P(className='text-ssindex-average',children="Average"), html.P("Social External"), html.P("Complaints"), html.P("Texas"), html.P("Houston"), html.P("24/04/24"), html.P("Facebook")],
               ]
data = [
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="01"),
            html.P(className='text-primary align-middle mb-0', children="Environment"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-average border border-dark border-4 w-100 h-100", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="02"),
            html.P(
                className='text-primary align-middle mb-0', children="Social Capital"
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="03"),
            html.P(
                className='text-primary align-middle mb-0', children="Human Capital"
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average opacity-40 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="04"),
            html.P(
                className='text-primary align-middle mb-0',
                children="Business Model & Innovation",
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="05"),
            html.P(
                className='text-primary align-middle mb-0',
                children="Leadership & Governance",
            ),
            html.Div(
                className="bg-ssindex-no-data opacity-40 w-100 h-100", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 border border-dark border-4",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="06"),
            html.P(className='text-primary align-middle mb-0', children="Others"),
            html.Div(
                className="bg-ssindex-no-data border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]

data_environment = [
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="0"),
            html.P(className='text-primary align-middle mb-0', children="Environment"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-average border border-dark border-4 w-100 h-100", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="1"),
            html.P(
                className='text-primary align-middle mb-0', children="Social Capital"
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="2"),
            html.P(
                className='text-primary align-middle mb-0', children="Human Capital"
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average opacity-40 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="3"),
            html.P(
                className='text-primary align-middle mb-0',
                children="Business Model & Innovation",
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="4"),
            html.P(
                className='text-primary align-middle mb-0',
                children="Leadership & Governance",
            ),
            html.Div(
                className="bg-ssindex-no-data opacity-40 w-100 h-100", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 border border-dark border-4",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary align-middle mb-0", children="5"),
            html.P(className='text-primary align-middle mb-0', children="Others"),
            html.Div(
                className="bg-ssindex-no-data border border-dark border-4 w-100 h-100",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-average w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-good w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100 opacity-40",
                children="\u200B",
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 text-center border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]

footer_data = [
    html.P(className='text-primary align-middle mb-0', children="Total Score"),
    "",
    "",
    "",
    "",
    "",
    "",
    html.Div(
        className="bg-ssindex-average w-100 h-100 text-center border rounded",
        children=html.B(className='text-white', children="45%"),
    ),
    html.Div(
        className="bg-ssindex-excellent w-100 h-100 text-center border rounded",
        children=html.B(className='text-white', children="20th"),
    ),
]

class_name_headers = 'bg-ssindex-table-header-gray'
class_name_headers_2 = 'bg-white'