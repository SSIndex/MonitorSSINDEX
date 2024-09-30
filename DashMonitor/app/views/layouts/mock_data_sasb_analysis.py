'''
Temporary file to hold mock data for SASB Analysis
'''

# 3rd party imports
from dash import html


# Example data for custom components
company_name = 'Webster Bank'  # 'Webster Bank'
industry = 'Bank'
country = 'EEUU'
company_image = 'https://wallpaperaccess.com/full/1642272.jpg'
overview = 'Medium'
overview_text = 'This company holds a medium sentiment score. Feedback is evenly split, with 50% of comments being positive and 50% negative. This indicates a balanced perception among respondents.'

headers = [
    html.P(className="text-primary mb-0", children="#"),
    html.P(className="text-primary mb-0", children="Dimension ESG"),
    html.P(className="text-ssindex-graph-grey mb-0", children="No Data"),
    html.P(
        className="text-ssindex-poor mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0", children="Poor"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="0-19%"),
            ]
        ),
    ),
    html.P(
        className="text-ssindex-low mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0", children="Low"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="20-39%"),
            ]
        ),
    ),
    html.P(
        className="text-ssindex-average mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0 ", children="Average"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="40-59%"),
            ]
        ),
    ),
    html.P(
        className="text-ssindex-good mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0", children="Good"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="60-79%"),
            ]
        ),
    ),
    html.P(
        className="text-ssindex-excellent mb-0",
        children=html.Div(
            children=[
                html.P(className="m-0", children="Excellent"),
                html.P(className='fw-normal m-0 fs-7 text-dark', children="80-100%"),
            ]
        ),
    ),
    "Score",
    html.P(
        className="mb-0",
        children=html.Div(
            children=[
                html.Div(className="m-0", children="Percentil"),
                html.P(
                    className='fw-normal m-0 fs-7 text-dark', children="Local Industry"
                ),
            ]
        ),
    ),
]
nested_headers = [
    "Review",
    "Sentiment Score",
    "Category",
    "ESG Pilar",
    "Dimension",
    "Territory or State",
    "City",
    "Date",
    "Source",
]
nested_data = [
    [
        html.P(children="I called and called an no one answered the phone"),
        html.P("8%"),
        html.P(className="text-ssindex-poor", children="Poor"),
        html.P("Social External"),
        html.P("Complaints"),
        html.P("New York"),
        html.P("New York"),
        html.P("12/08/23"),
        html.P("Google"),
    ],
    [
        html.P("I called and called an no one answered the phone"),
        html.P("12%"),
        html.P(className="text-ssindex-poor", children="Poor"),
        html.P("Social External"),
        html.P("Complaints"),
        html.P("California"),
        html.P("Los Angeles"),
        html.P("05/07/24"),
        html.P("Instagram"),
    ],
    [
        html.P(
            "I had a problem with one of the products, called, no one answered, then sent an email and the got back to me in two days. Fortunately the problem was solved"
        ),
        html.P("54%"),
        html.P(className='text-ssindex-average', children="Average"),
        html.P("Social External"),
        html.P("Complaints"),
        html.P("Texas"),
        html.P("Houston"),
        html.P("24/04/24"),
        html.P("Facebook"),
    ],
]
data = [
    {
        "data": [
            html.P(className="text-primary mb-0", children="01"),
            html.P(className='text-primary mb-0', children="Environment"),
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
                className="bg-ssindex-average border border-dark border-4 w-100 h-100",
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
                className="bg-ssindex-average w-100 h-100  border rounded",
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
            html.P(className="text-primary mb-0", children="02"),
            html.P(className='text-primary mb-0', children="Social Capital"),
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
            html.P(className="text-primary mb-0", children="03"),
            html.P(className='text-primary mb-0', children="Human Capital"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4",
                children="\u200B",
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
                className="bg-ssindex-low w-100 h-100  border rounded",
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
            html.P(className="text-primary mb-0", children="04"),
            html.P(
                className='text-primary mb-0',
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
            html.P(className="text-primary mb-0", children="05"),
            html.P(
                className='text-primary mb-0',
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
            html.P(className="text-primary mb-0", children="06"),
            html.P(className='text-primary mb-0', children="Others"),
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
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]

data_environment = [
    {
        "data": [
            html.P(className="text-primary mb-0", children="01"),
            html.P(className='text-primary mb-0', children="GHG Emissions"),
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
                className="bg-ssindex-average border border-dark border-4 w-100 h-100",
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
                className="bg-ssindex-average w-100 h-100  border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="02"),
            html.P(className='text-primary mb-0', children="Air Quality"),
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
                className="bg-ssindex-poor w-100 h-100  border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="03"),
            html.P(className='text-primary mb-0', children="Energy Management"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4",
                children="\u200B",
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
                className="bg-ssindex-low w-100 h-100  border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="04"),
            html.P(
                className='text-primary mb-0',
                children="Water & Wastewater Management",
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
                className="bg-ssindex-good w-100 h-100  border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="05"),
            html.P(
                className='text-primary mb-0',
                children="Waste & Hazardous Material Management",
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
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="06"),
            html.P(className='text-primary mb-0', children="Ecological Impacts"),
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
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="07"),
            html.P(className='text-primary mb-0', children="Others"),
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
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]

data_social_capital = [
    {
        "data": [
            html.P(className="text-primary mb-0", children="01"),
            html.P(
                className='text-primary mb-0',
                children="Human Rights & Community Relations",
            ),
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
                className="bg-ssindex-average border border-dark border-4 w-100 h-100",
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
                className="bg-ssindex-average w-100 h-100  border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="02"),
            html.P(className='text-primary mb-0', children="Customer Privacy"),
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
                className="bg-ssindex-poor w-100 h-100  border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="03"),
            html.P(className='text-primary mb-0', children="Data Security"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4",
                children="\u200B",
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
                className="bg-ssindex-low w-100 h-100  border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="04"),
            html.P(
                className='text-primary mb-0',
                children="Access & Affordability",
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
                className="bg-ssindex-good w-100 h-100  border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="05"),
            html.P(
                className='text-primary mb-0',
                children="Product Quality & Safety",
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
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="06"),
            html.P(className='text-primary mb-0', children="Customer Welfare"),
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
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="07"),
            html.P(
                className='text-primary mb-0',
                children="Selling Practices & Product Labeling",
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
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="08"),
            html.P(className='text-primary mb-0', children="Others"),
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
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]

data_human_capital = [
    {
        "data": [
            html.P(className="text-primary mb-0", children="01"),
            html.P(className='text-primary mb-0', children="Labor Practices"),
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
                className="bg-ssindex-average border border-dark border-4 w-100 h-100",
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
                className="bg-ssindex-average w-100 h-100  border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="02"),
            html.P(className='text-primary mb-0', children="Employee Health & Safety"),
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
                className="bg-ssindex-poor w-100 h-100  border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="03"),
            html.P(
                className='text-primary mb-0',
                children="Employee Engagement, Diversity & Inclusion",
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4",
                children="\u200B",
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
                className="bg-ssindex-low w-100 h-100  border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="04"),
            html.P(
                className='text-primary mb-0',
                children="Others",
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
                className="bg-ssindex-good w-100 h-100  border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
]

data_business_model_innovation = [
    {
        "data": [
            html.P(className="text-primary mb-0", children="01"),
            html.P(
                className='text-primary mb-0',
                children="Product Desing & Lifecycle  Management",
            ),
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
                className="bg-ssindex-average border border-dark border-4 w-100 h-100",
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
                className="bg-ssindex-average w-100 h-100  border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="02"),
            html.P(className='text-primary mb-0', children="Business Model Resilience"),
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
                className="bg-ssindex-poor w-100 h-100  border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="03"),
            html.P(className='text-primary mb-0', children="Supply Chain Management"),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4",
                children="\u200B",
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
                className="bg-ssindex-low w-100 h-100  border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="04"),
            html.P(
                className='text-primary mb-0',
                children="Materials Sourcing & Efficiency",
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
                className="bg-ssindex-good w-100 h-100  border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="05"),
            html.P(
                className='text-primary mb-0',
                children="Physical Impacts of Climate Change",
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
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="06"),
            html.P(className='text-primary mb-0', children="Others"),
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
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]

data_leadership_governance = [
    {
        "data": [
            html.P(className="text-primary mb-0", children="01"),
            html.P(className='text-primary mb-0', children="Business Ethics"),
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
                className="bg-ssindex-average border border-dark border-4 w-100 h-100",
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
                className="bg-ssindex-average w-100 h-100  border rounded",
                children=html.B(className='text-white', children="45%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="02"),
            html.P(className='text-primary mb-0', children="Competitive Behaviour"),
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
                className="bg-ssindex-poor w-100 h-100  border rounded",
                children=html.B(className='text-white', children="15%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ],
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="03"),
            html.P(
                className='text-primary mb-0',
                children="Managament of The Legal and Regulatory Environment",
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-poor w-100 h-100 opacity-40", children="\u200B"
            ),
            html.Div(
                className="bg-ssindex-low w-100 h-100 border border-dark border-4",
                children="\u200B",
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
                className="bg-ssindex-low w-100 h-100  border rounded",
                children=html.B(className='text-white', children="30%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="04"),
            html.P(
                className='text-primary mb-0',
                children="Critical Incident Risk Management",
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
                className="bg-ssindex-good w-100 h-100  border rounded",
                children=html.B(className='text-white', children="65%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="05"),
            html.P(
                className='text-primary mb-0',
                children="Systemic Risk Management",
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
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="95%"),
            ),
            html.Div(
                className="bg-ssindex-excellent w-100 h-100  border rounded",
                children=html.B(className='text-white', children="20th"),
            ),
        ]
    },
    {
        "data": [
            html.P(className="text-primary mb-0", children="06"),
            html.P(className='text-primary mb-0', children="Others"),
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
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0%"),
            ),
            html.Div(
                className="bg-ssindex-no-data w-100 h-100  border rounded",
                children=html.B(className='text-white', children="0th"),
            ),
        ]
    },
]

footer_data = [
    html.P(className='text-primary mb-0', children="Total Score"),
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    html.Div(
        className="bg-ssindex-average w-100 h-100  border rounded",
        children=html.B(className='text-white', children="45%"),
    ),
    html.Div(
        className="bg-ssindex-excellent w-100 h-100  border rounded",
        children=html.B(className='text-white', children="20th"),
    ),
]

class_name_headers = 'bg-ssindex-table-header-gray'
class_name_headers_2 = 'bg-white'

mock_score = 44
mock_score_text = html.B(
    className='text-ssindex-average',
    children='Average',
)
mock_min_value = 0
mock_max_value = 100
mock_labels = [
        html.B(className='text-ssindex-poor', children='Poor'),
        html.B(className='text-ssindex-low', children='Low'),
        html.B(className='text-ssindex-average', children='Average'),
        html.B(className='text-ssindex-good', children='Good'),
        html.B(className='text-ssindex-excellent', children='Excellent'),
    ]

mock_score_labels = [
    html.P(className='text-secondary', children='[0-19]'),
    html.P(className='text-secondary', children='[20-39]'),
    html.P(className='text-secondary', children='[40-59]'),
    html.P(className='text-secondary', children='[60-70]'),
    html.P(className='text-secondary', children='[80-100]'),
]
