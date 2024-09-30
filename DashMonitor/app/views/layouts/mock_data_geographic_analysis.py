'''
Temporary file to hold mock data for geographic analysis
'''

# 3rd party imports
from dash import html


headers = [
    html.P(className="text-primary mb-0", children="Color"),
    html.P(className="text-primary mb-0", children="Region/State"),
    html.P(className="text-primary mb-0", children="Score"),
    html.P(className="text-primary mb-0", children="Percentil"),
]

nested_headers = ["Comment", "Score", "Category", "City", "Date", "Source"]
nested_data = [
    [
        html.P(children="I called and called an no one answered the phone"),
        html.P("8%"),
        html.P("Social External"),
        html.P("New York"),
        html.P("12/08/23"),
        html.P("Google"),
    ],
    [
        html.P("I called and called an no one answered the phone"),
        html.P("12%"),
        html.P("Social External"),
        html.P("Los Angeles"),
        html.P("05/07/24"),
        html.P("Instagram"),
    ],
    [
        html.P(
            "I had a problem with one of the products, called, no one answered, then sent an email and the got back to me in two days. Fortunately the problem was solved"
        ),
        html.P("54%"),
        html.P("Social External"),
        html.P("Houston"),
        html.P("24/04/24"),
        html.P("Facebook"),
    ],
]
data = [
    {
        "data": [
            html.Div(
                className="bg-ssindex-excellent border border-dark border-4",
                style={
                    "width": "50px",
                    "height": "50px",
                    "border-radius": "50%",
                    "display": "inline-block",
                },
                children=html.P("\u200B"),
            ),
            html.P("New York"),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.Div(
                className="bg-ssindex-low border border-dark border-4",
                style={
                    "width": "50px",
                    "height": "50px",
                    "border-radius": "50%",
                    "display": "inline-block",
                },
                children=html.P("\u200B"),
            ),
            html.P("California"),
            html.Div(
                className="bg-ssindex-low w-100 h-100  border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.Div(
                className="bg-ssindex-poor border border-dark border-4",
                style={
                    "width": "50px",
                    "height": "50px",
                    "border-radius": "50%",
                    "display": "inline-block",
                },
                children=html.P("\u200B"),
            ),
            html.P("Texas"),
            html.Div(
                className="bg-ssindex-poor w-100 h-100  border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.Div(
                className="bg-ssindex-good border border-dark border-4",
                style={
                    "width": "50px",
                    "height": "50px",
                    "border-radius": "50%",
                    "display": "inline-block",
                },
                children=html.P("\u200B"),
            ),
            html.P("Washington"),
            html.Div(
                className="bg-ssindex-good w-100 h-100  border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.Div(
                className="bg-ssindex-average border border-dark border-4",
                style={
                    "width": "50px",
                    "height": "50px",
                    "border-radius": "50%",
                    "display": "inline-block",
                },
                children=html.P("\u200B"),
            ),
            html.P("Florida"),
            html.Div(
                className="bg-ssindex-average w-100 h-100  border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
        "nested_data": nested_data,
        "nested_headers": nested_headers,
    },
    {
        "data": [
            html.Div(
                className="bg-ssindex-excellent border border-dark border-4",
                style={
                    "width": "50px",
                    "height": "50px",
                    "border-radius": "50%",
                    "display": "inline-block",
                },
                children=html.P("\u200B"),
            ),
            html.P("Arizona"),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
]

class_name_headers = 'bg-ssindex-table-header-gray'
class_name_headers_2 = 'bg-white'
class_name_rows = 'd-flex justify-content-center'
