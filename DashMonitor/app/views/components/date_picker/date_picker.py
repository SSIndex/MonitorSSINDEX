from DashMonitor.app.views.components.base_component import BaseComponent
from dash import html, dcc
from datetime import date, timedelta

from DashMonitor.app.views.components.utils.button import ButtonUtils


class DatePicker(BaseComponent):
    '''
    Date Picker Component. Generates a date picker component which allows the user to select a date
    and predefined ranges like 'Today', '5 days', etc.

    Parameters
    ----------
    disabled : bool
        If True, the Date Picker is disabled and cannot be interacted with. Default is False.
    '''

    # Constants for labels and button IDs
    BUTTON_LABELS = ['Today', '5 days', '1 month', '3 months', '6 months', '1 year']
    BUTTON_IDS = [f'btn-nclicks-{i}' for i in range(len(BUTTON_LABELS))]

    def __init__(self, disabled=False):
        self.disabled = disabled

    def render(self):
        # Determine the button classes and attributes based on the disabled state
        button_class = (
            'btn m-1 ms-2 border border-dark text-ssindex-graph-grey'
            if not self.disabled
            else 'btn m-1 ms-1 text-ssindex-graph-grey border border-0'
        )

        return html.Div(
            children=[
                html.Label('Time Frame', className='form-label'),
                # Button to open DatePicker, initially shows the last year date range
                html.Button(
                    children=f'{date.today() - timedelta(days=365)} - {date.today()}',
                    id='date-picker-button' if not self.disabled else '',
                    className=button_class,
                    disabled=self.disabled,
                    **{
                        'data-bs-toggle': 'collapse',
                        'data-bs-target': '#date-picker-container',
                    },
                ),
                # Collapsible container for Date Picker (only renders if not disabled)
                (
                    html.Div(
                        id='date-picker-container',
                        className='collapse z-3 position-absolute bg-white border rounded shadow-lg w-25',
                        children=[
                            html.Div(
                                className='d-flex flex-column mt-4 mb-3 p-1',
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
                                                        className=ButtonUtils.STYLE_UNSELECTED_BUTTON,
                                                        id=btn_id,
                                                        n_clicks=0,
                                                    )
                                                    for label, btn_id in zip(
                                                        self.BUTTON_LABELS,
                                                        self.BUTTON_IDS,
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
                    )
                    if not self.disabled
                    else None
                ),
            ]
        )
