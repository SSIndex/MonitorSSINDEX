
from dash import html
from DashMonitor.app.views.components.base_component import BaseComponent


class Card(BaseComponent):

    _BASE_CARD_CLASS_NAME = 'card text-bg-primary'
 
    def __init__(self, company_name: str, industry: str, country: str, company_image: str, overview: str, overview_text: str, overview_graph: BaseComponent, text_color: str = None, background_color: str = None):
        self.company_name = company_name
        self.industry = industry
        self.country = country
        self.company_image = company_image
        self.overview = overview
        self.overview_text = overview_text
        self.overview_graph = overview_graph
        self.class_name = f'card {background_color}' if background_color else self._BASE_CARD_CLASS_NAME
        self.class_name = f'{self.class_name} {text_color}' if text_color else self.class_name

    def render(self) -> html.Div:
        return html.Div(
            className=self.class_name,
            children=[
                html.Div(
                    className='card-body',
                    children=[
                        html.Div(
                            className="row gx-5 pt-3 pb-3 ps-5 pe-5",
                            children=[
                                html.Div(
                                    className="col-6",
                                    children=[
                                        html.Div(
                                            className='d-flex gap-4 align-items-center',
                                            children=[
                                                html.Img(
                                                    src=self.company_image,
                                                    className='rounded-circle img-fluid',
                                                    width='158px',
                                                    alt='Company Image'
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.H3(self.company_name),
                                                        html.P(self.industry),
                                                        html.P(self.country)
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            children=[
                                                html.P(children = [html.P(children=[html.Span(
                                                    className="fw-bold",
                                                    children=f"Overview: {self.overview}. "
                                                    ),
                                                    self.overview_text])], className='mt-2'),
                                            ]
                                        )],
                                    ),
                                html.Div(
                                    className="col-6 border rounded",
                                    children=[self.overview_graph]
                                )
                            ]
                        )
                    ],
                )
            ],
        )
