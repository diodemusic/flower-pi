from jinja2 import Environment, FileSystemLoader
import os

env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "..", "templates"))
)


def render_template(template_name, **context):
    template = env.get_template(template_name)
    return template.render(**context)
