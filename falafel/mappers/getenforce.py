"""
getenforce - command ``/usr/sbin/getenforce``
=============================================

This very simple mapper returns the output of the ``getenforce`` command.

Examples:

    >>> enforce = shared[getenforcevalue]
    >>> enforce['status']
    'Enforcing'
"""

from .. import mapper


@mapper('getenforce')
def getenforcevalue(context):
    """
    The output of "getenforce" command is in one of "Enforcing", "Permissive",
    or "Disabled", so we can return the content directly.
    """
    return {"status": context.content[0]}