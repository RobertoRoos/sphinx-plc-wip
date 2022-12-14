import os
from typing import Dict
from sphinx.application import Sphinx

from .analyzer import PlcAnalyzer
from .domain import StructuredTextDomain
from .directives import PlcAutoFunctionBlock


def plcdoc_setup(app: Sphinx) -> Dict:
    """Initialize Sphinx extension."""

    # We place a callback for Sphinx for when the builder is about ready to start to index the PLC files
    # The moment of reading the PLC files could probably be anything.

    app.connect("builder-inited", analyze)

    app.add_config_value("plc_sources", [], True)  # List[str]

    app.add_domain(StructuredTextDomain)

    app.add_directive_to_domain("plc", "autofunctionblock", PlcAutoFunctionBlock)
    # app.add_directive("plcautofunctionblock", FunctionBlockDirective)

    return {
        "version": "0.0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def analyze(app: Sphinx):
    """Perform the analysis of PLC source and extract docs."""

    source_paths = (
        [app.config.plc_sources]
        if isinstance(app.config.plc_sources, str)
        else app.config.plc_sources
    )

    abs_source_paths = [
        os.path.normpath(os.path.join(app.confdir, path)) for path in source_paths
    ]

    app._plcdoc_analyzer = PlcAnalyzer(abs_source_paths, app)
