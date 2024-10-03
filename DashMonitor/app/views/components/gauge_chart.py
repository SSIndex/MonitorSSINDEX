from typing import List, Any, Optional

from dash import html

from DashMonitor.app.handlers.function_utils import categorize_score_to_text_class_name


class GaugeChart:
    """
    GaugeChart component to visualize a score along a gradient bar with labeled markers.

    Parameters
    ----------
    score : int
        The score to display on the gauge.
    score_text : str
        Text description of the score (e.g., 'Good', 'Excellent').
    min_value : int, optional
        The minimum value of the gauge (default is 0 if not provided).
    max_value : int, optional
        The maximum value of the gauge (default is 100 if not provided).
    labels : List[Any], optional
        A list of elements representing text labels for different score ranges on the gauge 
        (e.g., ['Poor', 'Low', 'Average', 'Good', 'Excellent']). If not provided, DEFAULT_LABELS are used.
    score_labels : List[Any], optional
        A list of elements representing the score ranges corresponding to the labels 
        (e.g., '[0-19]', '[20-39]'). If not provided, DEFAULT_SCORE_LABELS are used.

    Attributes
    ----------
    DEFAULT_LABELS : List[html.B]
        Default labels for score ranges (e.g., 'Poor', 'Low', 'Average', etc.).
    DEFAULT_SCORE_LABELS : List[html.P]
        Default labels for score ranges with numerical values (e.g., '[0-19]', '[20-39]', etc.).
    """
    DEFAULT_LABELS = [
        html.B(className='text-ssindex-poor', children='Poor'),
        html.B(className='text-ssindex-low', children='Low'),
        html.B(className='text-ssindex-average', children='Average'),
        html.B(className='text-ssindex-good', children='Good'),
        html.B(className='text-ssindex-excellent', children='Excellent'),
    ]

    DEFAULT_SCORE_LABELS = [
        html.P(className='text-secondary', children='[0-19]'),
        html.P(className='text-secondary', children='[20-39]'),
        html.P(className='text-secondary', children='[40-59]'),
        html.P(className='text-secondary', children='[60-70]'),
        html.P(className='text-secondary', children='[80-100]'),
    ]

    def __init__(
        self,
        score: int,
        score_text: str,
        min_value: Optional[int] = 0,
        max_value: Optional[int] = 100,
        labels: Optional[List[Any]] = None,
        score_labels: Optional[List[Any]] = None,
    ):
        self.score = score
        self.score_text = score_text
        self.min_value = min_value
        self.max_value = max_value
        self.text_labels = labels if labels else self.DEFAULT_LABELS
        self.score_labels = score_labels if score_labels else self.DEFAULT_SCORE_LABELS

    def _render_score_text(self) -> None:
        """
        Render the score text with a specific class name based on the score value.

        This method dynamically sets the CSS class based on the score (e.g., 'Good', 'Poor'),
        and updates the `self.score_text` with a bold styled HTML element.
        """
        text_class_name = categorize_score_to_text_class_name(self.score)
        self.score_text = html.B(className=text_class_name, children=self.score_text)

    def calculate_position(self) -> float:
        """Calculate the percentage position of the score along the bar."""
        return (self.score - self.min_value) / (self.max_value - self.min_value) * 100

    def render_score_display(self):
        """
        Render the numeric score and the score text description.

        This method creates the score marker (e.g., "85 / 100") along with the score's
        descriptive text (e.g., "Excellent"), all in a horizontally aligned layout.
        """
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
                            html.Span(className="text-ssindex-graph-grey",children=f" / {self.max_value}"),
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

    def render_labels(self, labels: List[str]) -> html.Div:
        """Render a row of labels (either above or below the gradient bar)."""
        return html.Div(
            className="d-flex justify-content-between w-100",
            children=[html.Span(label) for label in labels],
        )

    def render_gradient_bar(self) -> html.Div:
        """Render the gradient bar with a score marker."""
        score_position = self.calculate_position()
        # Gradient bar
        gradient_bar = html.Div(
            className="w-100 h-100 rounded",
            # Gradient style
            style={
                "background": "linear-gradient(to right, var(--bs-ssindex-poor), "
                "var(--bs-ssindex-average) 50%, var(--bs-ssindex-excellent))"
            },
            children="\u200B",
        )
        # Score marker (white circle) on top of the gradient bar
        score_marker = self.render_score_marker(score_position)

        return html.Div(
            className="w-100 position-relative mt-3 mb-3",
            children=[gradient_bar, score_marker],
        )

    def render_score_marker(self, score_position: float) -> html.Div:
        """Render a circular score marker at the calculated position."""
        return html.Div(
            className="position-absolute border border-dark border-4 bg-white rounded-circle",
            style={
                "top": "-8px",  # Adjust the vertical position above the bar
                "left": f"{score_position}%",  # Position based on the calculated score
                "transform": "translateX(-50%)",  # Center the circle
                "width": "40px",
                "height": "40px",
            },
        )

    def render(self) -> html.Div:
        """Render the complete gauge chart with score display, labels, and gradient bar."""
        self._render_score_text()
        return html.Div(
            className='text-center p-3',
            children=[
                self.render_score_display(),
                # Labels above the gradient bar
                self.render_labels(labels=self.text_labels),
                # Gradient bar with score marker
                self.render_gradient_bar(),
                # Score labels below the gradient bar
                self.render_labels(labels=self.score_labels),
            ],
        )
