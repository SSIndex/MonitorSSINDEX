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
    overview_text : str
        Text of the Overview
    overview_graph : BaseComponent
        Graph of the Overview Score
    text_color : Optional[str]
        Text Color of the Card. Ex: 'text-white'
    background_color : Optional[str]
        Background Color of the Card. Ex: 'bg-primary'
    """

    _BASE_CARD_CLASS_NAME = 'card text-bg-ssindex-card-blue rounded-3'

    def __init__(
        self,
        company_name: str,
        industry: str,
        country: str,
        company_image: str,
        overview: str,
        overview_text: str,
        overview_graph: BaseComponent,
        text_color: Optional[str] = None,
        background_color: Optional[str] = None,
    ):

        self.company_name = company_name
        self.industry = industry
        self.country = country
        self.company_image = company_image
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

    def render(self) -> html.Div:
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
                                            className='d-flex gap-4 align-items-center',
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
                                    className='col-6',
                                    children=[self.overview_graph],
                                ),
                            ],
                        )
                    ],
                )
            ],
        )
