def extract_original_error(error):
    if getattr(error, "original_error", None):
        return extract_original_error(error.original_error)
    return error
