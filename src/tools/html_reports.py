from jinja2 import Environment, FileSystemLoader, select_autoescape

JINJA_ENV = Environment(
    loader=FileSystemLoader("."),
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


# example usage:
# render BSI
# generate_html_with_results("jinja_templates/bsi_template.html.j2",
#                 {"tested_file": "some_file.rnd",
#                 "list_of_results": bsi_results},
#                 "generated_report_bsi.html")

# render FIPS
# generate_html_with_results("jinja_templates/fips_template.html.j2",
#                 {"tested_file": "some_file.rnd",
#                 "battery_accepted": True,
#                 "list_of_results": fips_results},
#                 "generated_report_fips.html")

# render NIST
# generate_html_with_results("jinja_templates/nist_template.html.j2",
#                 {"tested_file": "some_file.rnd",
#                 "list_of_results": nist_results},
#                 "generated_report_nist.html")


# render DieHarder
# generate_html_with_results("jinja_templates/dieharder_template.html.j2",
#                 {"tested_file": "some_file.rnd",
#                 "list_of_results": dieharder_results},
#                 "generated_report_dh.html")

# render TestU01
# generate_html_with_results("jinja_templates/testu01_template.html.j2",
#                 {"tested_file": "some_file.rnd",
#                  "list_of_results": testu01_results,
#                  "subbattery": "rabbit"},
#                 "generated_report_tu01.html")
