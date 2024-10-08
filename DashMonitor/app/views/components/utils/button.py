class ButtonUtils:
    '''Utility class for handling button-related operations.'''

    # Style classes for buttons
    STYLE_SELECTED_BUTTON = 'btn btn-primary m-1'
    STYLE_UNSELECTED_BUTTON = 'btn btn-outline-primary m-1'

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
                if ButtonUtils.STYLE_SELECTED_BUTTON in class_name
            ),
            -1,
        )
