from dash import html, dcc, Input, Output, ctx, callback, State
from datetime import date, timedelta
from DashMonitor.app.views.components.date_picker.date_picker import DatePicker


def calculate_date_range(selected_index: int) -> str:
    '''Calculate date range based on selected button.'''
    today = date.today()
    # Today button selected
    if selected_index == 0:
        return f"{today}"
    # Custom range selected from DATE_RANGES
    if selected_index in range(1, 6):
        start_date = today - timedelta(days=DatePicker.DATE_RANGES[selected_index - 1])
        return f"{start_date} - {today}"

    # Default label if no range is selected
    return f"{today - timedelta(days=365)} - {today}"


def register_datepicker_callbacks(app):

    @app.callback(
        Output('date-picker-button', 'children'),
        Input('submit-btn', 'n_clicks'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        [State(btn_id, 'className') for btn_id in DatePicker.BUTTON_IDS],
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
        return calculate_date_range(selected_index)

    @app.callback(
        [Output(btn_id, 'className') for btn_id in DatePicker.BUTTON_IDS],
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        [Input(btn_id, 'n_clicks') for btn_id in DatePicker.BUTTON_IDS],
    )
    def update_button_style(
        *button_clicks,
    ):
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
