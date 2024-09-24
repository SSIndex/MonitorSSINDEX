from DashMonitor.app.views.components.base_component import BaseComponent
from dash import html, dcc, Input, Output, ctx, callback, State


class DatePicker(BaseComponent):
    """
    Date Picker Component. Generates a date picker component which allows the user to select a date
    and predefined ranges like 'Today', '5 days', etc.
    """

    # Define class-level constants for labels and button IDs
    BUTTON_LABELS = ['Today', '5 days', '1 month', '3 months', '6 months', '1 year']
    BUTTON_IDS = [f'btn-nclicks-{i}' for i in range(len(BUTTON_LABELS))]

    def __init__(self):
        pass

    def render(self):
        return html.Div(
            className='d-flex flex-column mt-4 w-25 mb-5',
            children=[
                # Button Row
                html.Div(
                    className='row mb-3',
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
                    className='row',
                    children=[
                        html.Div(
                            className='col-12',
                            children=[
                                dcc.DatePickerRange(
                                    id='date-picker-range',
                                    clearable=True,
                                ),
                            ],
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
                # Output Divs
                html.Div(id='output-container-date-picker-range'),
            ],
        )

    @callback(
        Output('output-container-date-picker-range', 'children'),
        Input('submit-btn', 'n_clicks'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        [State(btn_id, 'className') for btn_id in BUTTON_IDS],
    )
    def display_submission_info(n_clicks, start_date, end_date, *button_classes):
        if start_date and end_date:
            return f'Searching data from {start_date} to {end_date}'
        # Check which predefined date button is selected
        selected_index = next(
            (
                i
                for i, class_name in enumerate(button_classes)
                if 'btn-primary' in class_name
            ),
            None,
        )
        if selected_index is not None:
            return f'Searching data for the last {DatePicker.BUTTON_LABELS[selected_index]}'
        return 'No data selected yet'

    @callback(
        [Output(btn_id, 'className') for btn_id in BUTTON_IDS],
        [Input(btn_id, 'n_clicks') for btn_id in BUTTON_IDS],
    )
    def update_button_style(*button_clicks):
        triggered_id = ctx.triggered_id
        # Default to outline for all buttons
        btn_classes = ['btn btn-outline-primary m-1'] * len(DatePicker.BUTTON_IDS)

        # Set clicked button to primary
        if triggered_id in DatePicker.BUTTON_IDS:
            btn_index = DatePicker.BUTTON_IDS.index(triggered_id)
            btn_classes[btn_index] = 'btn btn-primary m-1'

        return btn_classes
