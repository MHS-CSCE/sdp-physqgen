"""
Last Modified: May 8, 2024
"""

from physqgen.app.app import create_app
from physqgen.generator.config import copyQuestionImagesToServerFolder
from os.path import join
from physqgen.app.register_config import registerConfig

if __name__ == "__main__":
    # registers the config and associated global variable
    registerConfig(join(".", "configs"))
    copyQuestionImagesToServerFolder(join(".", "configs", "images"), join(".", "src", "physqgen", "app", "static", "images"))
    app = create_app()
    app.run(port=8080, host='0.0.0.0')
