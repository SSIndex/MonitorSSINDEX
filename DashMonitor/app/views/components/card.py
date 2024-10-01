from dash import html
from DashMonitor.app.views.components.base_component import BaseComponent
from typing import Optional


class Card(BaseComponent):
    """
    Card Component. Generates a card component which displays information of the company and its overview/score.

    Parameters
    ----------
    company_name : str
        Company Name
    industry : str
        Industry of the Company
    country : str
        Country of the Company
    company_image : str
        URL of the Company Image. It must be a square image.
    overview : str
        Overview of the Company: Ex: 'Average'
    overview_text : Optional[str]
        Text of the Overview
    overview_graph : BaseComponent
        Graph of the Overview Score
    text_color : Optional[str]
        Text Color of the Card. Ex: 'text-white'
    background_color : Optional[str]
        Background Color of the Card. Ex: 'bg-primary'
    """

    _BASE_CARD_CLASS_NAME = 'card text-bg-ssindex-card-blue rounded-3'
    mock_image = 'assets/boeing.png'

    def __init__(
        self,
        company_name: str,
        industry: str,
        country: str,
        company_image: str,
        overview: str,
        overview_graph: BaseComponent,
        overview_text: Optional[str] = None,
        text_color: Optional[str] = None,
        background_color: Optional[str] = None,
    ):

        self.company_name = company_name
        self.industry = industry
        self.country = country
        # self.company_image = company_image
        self.company_image = self.mock_image
        self.overview = overview
        self.overview_text = overview_text
        self.overview_graph = overview_graph
        self.class_name = (
            f'card {background_color}'
            if background_color
            else self._BASE_CARD_CLASS_NAME
        )
        self.class_name = (
            f'{self.class_name} {text_color}' if text_color else self.class_name
        )

    def _generate_overview_text(self) -> None:
        if self.overview == 'Poor':
            self.overview_text = ' This company holds a low sentiment score. Feedback is mostly negative, with 80% of comments being negative and 20% positive. This indicates a negative perception among respondents'
        
        elif self.overview in ['Average', 'Medium']:
            self.overview_text = ' This company holds a medium sentiment score. Feedback is evenly split, with 50% of comments being positive and 50% negative. This indicates a balanced perception among respondents'
        
        elif self.overview == 'Good':
            self.overview_text = ' This company holds a high sentiment score. Feedback is mostly positive, with 60% of comments being positive and 40% negative. This indicates a positive perception among respondents'
        
        elif self.overview == 'Excellent':
            self.overview_text = ' This company holds a very high sentiment score. Feedback is overwhelmingly positive, with 80% of comments being positive and 20% negative. This indicates a very positive perception among respondents'

    
    def render(self) -> html.Div:
        self._generate_overview_text()
        return html.Div(
            className=self.class_name,
            children=[
                html.Div(
                    className='card-body text-white',
                    children=[
                        html.Div(
                            className='row gx-5 pt-3 pb-3 ps-5 pe-5 align-items-center',
                            children=[
                                html.Div(
                                    className='col-6',
                                    children=[
                                        html.Div(
                                            className='d-flex gap-4',
                                            children=[
                                                html.Div(
                                                    html.Img(
                                                        src=self.company_image,
                                                        className='rounded-circle img-fluid',
                                                        width='158px',
                                                        alt='Company Image',
                                                    )
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.P(
                                                            self.company_name,
                                                            className='fs-3',
                                                        ),
                                                        html.P(
                                                            self.industry,
                                                            className='fs-5',
                                                        ),
                                                        html.P(
                                                            self.country,
                                                            className='fs-5',
                                                        ),
                                                    ]
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            children=[
                                                html.P(
                                                    children=[
                                                        html.P(
                                                            children=[
                                                                html.Span(
                                                                    className='fw-bold',
                                                                    children=f'Overview: {self.overview}. ',
                                                                ),
                                                                self.overview_text,
                                                            ]
                                                        )
                                                    ],
                                                    className='mt-2',
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className='col-6 border rounded-4 bg-white',
                                    children=[self.overview_graph],
                                ),
                            ],
                        )
                    ],
                )
            ],
        )
