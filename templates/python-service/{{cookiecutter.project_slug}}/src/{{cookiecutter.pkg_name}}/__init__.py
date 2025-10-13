"""{{ cookiecutter.pkg_name }} - {{ cookiecutter.project_description }}"""  # noqa: N999

__version__ = "0.1.0"


def hello() -> str:
    """Return a greeting message.

    Returns:
        A friendly greeting string.
    """
    return "Hello from {{ cookiecutter.pkg_name }}!"
