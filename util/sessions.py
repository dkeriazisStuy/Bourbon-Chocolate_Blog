def set_ret_path(session, path):
    """Set the return path in session `session` to `path`"""
    session['ret_path'] = path


def clear_ret_path(session):
    """Clear return path in session `session` if it exists"""
    if 'ret_path' in session:
        del session['ret_path']


def use_ret_path(session):
    """Return and delete return path from session `session` if it exists"""
    if 'ret_path' in session:
        ret_path = session['ret_path']
        del session['ret_path']
    else:
        ret_path = None
    return ret_path

