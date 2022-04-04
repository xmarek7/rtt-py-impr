import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

# search path is jinja_templates directory's absolute path
JINJA_SEARCH_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "jinja_templates"
)

# initialization of jinja environment
JINJA_ENV = Environment(
    loader=FileSystemLoader(JINJA_SEARCH_PATH),
    autoescape=select_autoescape())

def generate_html_with_results(html_template: str, variables: dict, rendered_result: str):
    """Take a jinja2 template and render it with provided variables.

    Args:
        html_template (str): Path to Jinja2 template
        variables (dict): Dictionary with keys as names of variables
            and values are regular Python variables.
        rendered_result (str): Specifies location of a rendered file
    """
    rendered_template = JINJA_ENV.get_template(html_template).render(variables)
    with open(rendered_result, 'w') as rendr:
        rendr.write(rendered_template)


def get_html_template_name(battery_name: str) -> str:
    """Get template name to use for 'generate_html_with_results' method
        based on a battery_name

    Args:
        battery_name (str): Name of a test battery

    Returns:
        str: Name of a template for battery's HTML report
    """
    if battery_name in ["small_crush", "crush",
                        "big_crush", "rabbit", "alphabit", "block_alphabit"]:
        return "testu01_template.html.j2"
    else:
        return f"{battery_name}_template.html.j2"
