from DashMonitor.app.views.components.date_picker.date_picker import DatePicker


class ButtonIndexGetter:
    '''Utility class for handling button-related operations.'''

    @staticmethod
    def selected_button_index(button_classes: list) -> int:
        '''
        Get the index of the selected button.

        Iterates through the list of button classes to find the first occurrence
        of the selected button style. Returns the index of the selected button,
        or -1 if no button is currently selected.
        '''
        return next(
            (
                i
                for i, class_name in enumerate(button_classes)
                if DatePicker.STYLE_SELECTED_BUTTON in class_name
            ),
            -1,
        )
