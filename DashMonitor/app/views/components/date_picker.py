from DashMonitor.app.views.components.base_component import BaseComponent
from dash import html, dcc, Input, Output, ctx, callback, State
from datetime import date, timedelta


class DatePicker(BaseComponent):
    '''
    Date Picker Component. Generates a date picker component which allows the user to select a date
    and predefined ranges like 'Today', '5 days', etc.
    '''

    # Constants for labels and button IDs
    BUTTON_LABELS = ['Today', '5 days', '1 month', '3 months', '6 months', '1 year']
    BUTTON_IDS = [f'btn-nclicks-{i}' for i in range(len(BUTTON_LABELS))]
    DATE_RANGES = [5, 30, 90, 180, 365]  # Corresponding ranges

    # Styles for predefined ranges buttons
    STYLE_SELECTED_BUTTON = 'btn btn-primary m-1'
    STYLE_UNSELECTED_BUTTON = 'btn btn-outline-primary m-1'

    def render(self):
        return html.Div(
            children=[
                html.Label('Time Frame:', className='form-label'),
                # Button to open DatePicker, initially shows the last year date range
                html.Button(
                    children=f'{date.today() - timedelta(days=365)} - {date.today()}',
                    id='date-picker-button',
                    className='btn btn-secondary m-1',
                    **{
                        'data-bs-toggle': 'collapse',
                        'data-bs-target': '#date-picker-container',
                    },
                ),
                # Collapsible container for Date Picker
                html.Div(
                    id='date-picker-container',
                    className='collapse',
                    children=[
                        html.Div(
                            className='d-flex flex-column mt-4 mb-5 border p-3',
                            style={'width': '30%'},
                            children=[
                                html.Div(
                                    className='mb-2',
                                    children=[
                                        # Buttons for predefined date ranges
                                        html.Div(
                                            className='text-center',
                                            children=[
                                                html.Button(
                                                    label,
                                                    type='button',
                                                    className=DatePicker.STYLE_UNSELECTED_BUTTON,
                                                    id=btn_id,
                                                    n_clicks=0,
                                                )
                                                for label, btn_id in zip(
                                                    self.BUTTON_LABELS, self.BUTTON_IDS
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                # Calendar Date Picker
                                html.Div(
                                    className='text-center',
                                    children=[
                                        dcc.DatePickerRange(
                                            id='date-picker-range',
                                            clearable=True,
                                        ),
                                    ],
                                ),
                                # Submit Filter Button
                                html.Div(
                                    className='text-center mt-3',
                                    children=[
                                        html.Button(
                                            'Search',
                                            className='btn btn-success m-1',
                                            id='submit-btn',
                                            n_clicks=0,
                                        )
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
            ]
        )

    @staticmethod
    def calculate_date_range(selected_index: int) -> str:
        '''Static helper method to calculate date range based on selected button.'''
        today = date.today()
        # Today button selected
        if selected_index == 0:
            return f"{today}"
        # Custom range selected from DATE_RANGES
        if selected_index in range(1, 6):
            start_date = today - timedelta(
                days=DatePicker.DATE_RANGES[selected_index - 1]
            )
            return f"{start_date} - {today}"

        # Default label if no range is selected
        return f"{today - timedelta(days=365)} - {today}"

    @callback(
        Output('date-picker-button', 'children'),
        Input('submit-btn', 'n_clicks'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        [State(btn_id, 'className') for btn_id in BUTTON_IDS],
    )
    def display_submission_info(
        n_clicks, start_date: str, end_date: str, *button_classes
    ):
        '''
        Display the existing date range filter in the Time Frame button.
        '''
        # Custom or single date range was manually selected
        if start_date:
            return f'{start_date} - {end_date}' if end_date else f'{start_date}'

        # Predefined button selected
        selected_index = next(
            (
                i
                for i, class_name in enumerate(button_classes)
                if DatePicker.STYLE_SELECTED_BUTTON in class_name
            ),
            None,
        )
        # Calculate date range based on selected button
        return DatePicker.calculate_date_range(selected_index)

    @callback(
        [Output(btn_id, 'className') for btn_id in BUTTON_IDS],
        [Input(btn_id, 'n_clicks') for btn_id in BUTTON_IDS],
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
    )
    def update_button_style(*button_clicks):
        '''
        Update button styles of predefined date ranges. If a button is clicked, it will be highlighted.
        '''
        # Default to outline for all buttons
        btn_classes = [DatePicker.STYLE_UNSELECTED_BUTTON] * len(DatePicker.BUTTON_IDS)
        triggered_id = ctx.triggered_id
        # Set clicked button to primary
        if triggered_id in DatePicker.BUTTON_IDS:
            btn_index = DatePicker.BUTTON_IDS.index(triggered_id)
            btn_classes[btn_index] = DatePicker.STYLE_SELECTED_BUTTON
        return btn_classes
