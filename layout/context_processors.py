def active_url(request):
    """
    Add current request path to context
    """
    path = request.path
    return {'current_path': path}
