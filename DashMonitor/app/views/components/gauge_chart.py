from dash import html


class GaugeChart:
    # TODO: ADD DOCS and type hints, and refactor styles
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

    def __init__(self, score, score_text, min_value, max_value, labels, score_labels):
        # TODO: when not using mock data, uncomment the following lines
        # self.score = score
        # self.score_text = score_text
        # self.min_value = min_value
        # self.max_value = max_value
        # self.text_labels = labels
        # self.score_labels = score_labels
        self.score = self.mock_score
        self.score_text = self.mock_score_text
        self.min_value = self.mock_min_value
        self.max_value = self.mock_max_value
        self.text_labels = self.mock_labels
        self.score_labels = self.mock_score_labels


    def calculate_position(self):
        """Calculate the percentage position of the score along the bar."""
        return (self.score - self.min_value) / (self.max_value - self.min_value) * 100

    def render_score_display(self):
        """Render the score and score text display."""
        return html.Div(
            className='d-flex justify-content-between align-items-center p-3',
            children=[
                # Current score marker with different styles for score and max_value
                html.Div(
                    className='text-primary',
                    children=html.P(
                        className='text-primary m-0',  # Remove default margin for better alignment
                        children=[
                            html.Span(
                                className='fs-1 fw-bold', children=f"{self.score}"
                            ),
                            html.Span(
                                f" / {self.max_value}", style={'font-size': '1rem'}
                            ),  # Normal size for max_value
                        ],
                    ),
                ),
                # The score text
                html.Div(
                    className='text-primary',
                    children=html.H2(
                        className="text-primary m-0", children=self.score_text
                    ),
                ),
            ],
        )

    def render_labels(self, labels):
        """Render the labels above and below the gradient bar."""
        return html.Div(
            className="d-flex justify-content-between text-primary",
            style={"width": "100%"},
            children=[html.Span(label) for label in labels],
        )

    def render_gradient_bar(self):
        """Render the gradient bar with a score marker."""
        score_position = self.calculate_position()

        return html.Div(
            className="w-100 position-relative",
            style={"height": "30px", "margin": "10px 0"},
            children=[
                # Gradient bar
                html.Div(
                    className="w-100 h-100",
                    style={
                        "background": "linear-gradient(to right, var(--bs-ssindex-poor), "
                        "var(--bs-ssindex-average) 50%, var(--bs-ssindex-excellent))",
                    },
                    children="\u200B",
                ),
                # Score marker (white circle) on top of the gradient bar
                self.render_score_marker(score_position),
            ],
        )

    def render_score_marker(self, score_position):
        """Render the score marker (circle) on the gradient bar."""
        return html.Div(
            className="position-absolute",
            style={
                "top": "-5px",  # Adjust the vertical position above the bar
                "left": f"{score_position}%",  # Position based on the calculated score
                "transform": "translateX(-50%)",  # Center the circle
                "width": "40px",
                "height": "40px",
                "border-radius": "50%",
                "background-color": "white",
                "border": "4px solid black",  # Optional border for better visibility
            },
        )

    def render(self):
        """Render the entire GaugeChart component."""
        return html.Div(
            className='text-center p-3',
            children=[
                self.render_score_display(),
                # Labels above the gradient bar
                self.render_labels(
                    labels=self.text_labels
                ),
                # Gradient bar with score marker
                self.render_gradient_bar(),
                # Score labels below the gradient bar
                self.render_labels(
                    labels=self.score_labels
                ),
            ],
        )
