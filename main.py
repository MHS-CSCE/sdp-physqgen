"""
Last Modified: May 9, 2024
"""

from os.path import join

from physqgen.app.app import create_app
from physqgen.generator.config import (copyQuestionImagesToServerFolder,
                                       registerConfig)

if __name__ == "__main__":
    # registers the config and associated global variable
    registerConfig(join(".", "configs"))
    copyQuestionImagesToServerFolder(join(".", "configs", "images"), join(".", "src", "physqgen", "app", "static", "images"))
    app = create_app()
    app.run(port=8080, host='0.0.0.0')
