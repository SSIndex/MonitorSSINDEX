'''
GENERAL Analysis Layout
'''

# std imports

# 3rd party imports
from dash import html

# local imports


GENERAL_ANALYSIS_LAYOUT = html.Div(
    className='container',
    children=[
        html.Section(
            className='section bg-light pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-12 justify-content-end',
                                    children=[
                                        html.P(
                                            children=[
                                                '2024-06-12'
                                            ]  # Here Goes the Date of last data extracted
                                        )
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-6',
                                    children=[
                                        html.Div(
                                            className='row',
                                            children=[
                                                html.H4(children=['GlassCo SPA'])
                                            ],  # Here goes Company Name
                                        ),
                                        html.Div(
                                            className='row',
                                            children=[
                                                html.P(
                                                    children=[
                                                        'Glass Industry | Chile | Glass Market'
                                                    ]
                                                )
                                            ],  # Here goes Company Details
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className='col-6',
                                    children=['HERE GOES OVERALL SCORE'],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-white pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-2',
                                    children=[
                                        html.H6(
                                            className='text-end',
                                            children=['ESG COMPASS Overview:'],
                                        )
                                    ],
                                ),
                                html.Div(
                                    className='col-10',
                                    children=[
                                        html.P(
                                            className='text-center',
                                            children=[
                                                'HERE GOES THE OVERVIEW VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY LONG TEXT'
                                            ],
                                        )  # Here goes the overview description
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-6',
                                    children=[
                                        'HERE GOES SENTIMENT NORMALIZED HISTOGRAM (Y ranges from 0% to minimum between 100%, and max value of histogram )'
                                    ],
                                ),
                                html.Div(
                                    className='col-6',
                                    children=[
                                        'HERE GOES SENTIMENT RANKS TABLE',
                                        'POSICIÓN y PERCENTIL de: PROMEDIO UNIVERSO, PROMEDIO INDUSTRIA, SCORE EMPRESA',
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-light pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        'Analisis SASB',
                        'Tabla con columnas: Pilar | Porcentaje Comentarios del Pilar con respecto a Total Comentarios Empresa | Score | Grafica Categorización'
                        'Añadir Pilar Otros: Comentarios que no caen dentro de los pilares del análisis de ASG',
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-white pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        'Analisis SSINDEX',
                        'Mismos comentarios que análisis SASB',
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-light pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        'Analisis Detallado SASB',
                        'Columnas: Dimension | Porcentaje Comentarios del Pilar con respecto a Total | Puntaje | Categorizacion',
                    ],
                )
            ],
        ),
        html.Section(
            className='section bg-white pt-3',
            children=[
                html.Div(
                    className='container border-bottom border-dark',
                    children=[
                        'Analisis Detallado SSINDEX',
                        'Mismos comentarios de Analisis detallado SASB',
                    ],
                )
            ],
        ),
    ],
)
