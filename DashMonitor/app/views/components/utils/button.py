class ButtonUtils:
    '''Utility class for handling button-related operations.'''

    STYLE_SELECTED_BUTTON = 'btn btn-primary m-1'
    STYLE_UNSELECTED_BUTTON = 'btn btn-outline-primary m-1'

    @staticmethod
    def selected_button_index(button_classes: list) -> int:
        '''Get the index of the selected button. Returns -1 if no button is selected.'''
        return next(
            (i for i, class_name in enumerate(button_classes) if ButtonUtils.STYLE_SELECTED_BUTTON in class_name),
            -1,
        )