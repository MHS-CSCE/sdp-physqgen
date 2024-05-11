"""
Last Modified: May 11, 2024
"""
from os.path import join

from physqgen.database import createDatabase

if __name__ == "__main__":
    createDatabase(join(".", "data", "data.db"))
