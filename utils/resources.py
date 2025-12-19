import os
import sys

class Utils():

    @staticmethod
    def resource_path(rel_path: str) -> str:
        base = getattr(sys, "_MEIPASS", os.path.abspath("."))
        return os.path.join(base, rel_path)
