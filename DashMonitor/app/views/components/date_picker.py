from DashMonitor.app.views.components.base_component import BaseComponent
from dash import html, dcc, Input, Output, ctx, callback, State
from datetime import date, timedelta


class DatePicker(BaseComponent):
    """
    Date Picker Component. Generates a date picker component which allows the user to select a date
    and predefined ranges like 'Today', '5 days', etc.
    """

    # Constants for labels and button IDs
    BUTTON_LABELS = ['Today', '5 days', '1 month', '3 months', '6 months', '1 year']
    BUTTON_IDS = [f'btn-nclicks-{i}' for i in range(len(BUTTON_LABELS))]

    def __init__(self):
        pass

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
                                        html.Div(
                                            className='text-center',
                                            children=[
                                                html.Button(
                                                    label,
                                                    type='button',
                                                    className='btn btn-outline-primary m-1',
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
                                # Date Picker
                                html.Div(
                                    className='text-center',
                                    children=[
                                        dcc.DatePickerRange(
                                            id='date-picker-range',
                                            clearable=True,
                                        ),
                                    ],
                                ),
                                # Submit Button
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

    @callback(
        Output('date-picker-button', 'children'),
        Input('submit-btn', 'n_clicks'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        [State(btn_id, 'className') for btn_id in BUTTON_IDS],
    )
    def display_submission_info(n_clicks, start_date, end_date, *button_classes):
        today = date.today()

        # If a custom date range was manually selected
        if start_date and end_date:
            # Show the selected range as "start-date - end-date"
            date_range_text = f'{start_date} - {end_date}'

            # Change the button style to outline
            return date_range_text

        # Check which predefined date button is selected
        selected_index = next(
            (
                i
                for i, class_name in enumerate(button_classes)
                if 'btn-primary' in class_name
            ),
            None,
        )

        # Calculate the date ranges based on the selected button
        if selected_index is not None:
            if selected_index == 0:  # Today
                return f"{today}"
            elif selected_index == 1:  # Last 5 days
                start_date = today - timedelta(days=5)
                return f"{start_date} - {today}"
            elif selected_index == 2:  # Last 1 month
                start_date = today - timedelta(days=30)
                return f"{start_date} - {today}"
            elif selected_index == 3:  # Last 3 months
                start_date = today - timedelta(days=90)
                return f"{start_date} - {today}"
            elif selected_index == 4:  # Last 6 months
                start_date = today - timedelta(days=180)
                return f"{start_date} - {today}"
            elif selected_index == 5:  # Last 1 year
                start_date = today - timedelta(days=365)
                return f"{start_date} - {today}"

        # Default return if nothing is selected
        default_label = (
            f"{today - timedelta(days=365)} - {today}"  # Default button label (1 year)
        )
        return default_label

    @callback(
        [Output(btn_id, 'className') for btn_id in BUTTON_IDS],
        [Input(btn_id, 'n_clicks') for btn_id in BUTTON_IDS],
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
    )
    def update_button_style(*button_clicks):
        # Default to outline for all buttons
        btn_classes = ['btn btn-outline-primary m-1'] * len(DatePicker.BUTTON_IDS)
        triggered_id = ctx.triggered_id
        # Set clicked button to primary
        if triggered_id in DatePicker.BUTTON_IDS:
            btn_index = DatePicker.BUTTON_IDS.index(triggered_id)
            btn_classes[btn_index] = 'btn btn-primary m-1'
        return btn_classes
