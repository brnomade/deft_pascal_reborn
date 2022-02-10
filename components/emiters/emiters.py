"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2021- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import os
import logging
from jinja2 import Template

template_program_heading = """
{% for header in header_files %}
    #include <{{header}}.h>
{% endfor %}
"""

t = Template()


