def extract_original_error(error):
    if getattr(error, "original_error", None) is not None:
        return extract_original_error(error.original_error)
    return error
