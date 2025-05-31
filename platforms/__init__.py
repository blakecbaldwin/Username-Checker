import os
import importlib

platform_checkers = {}
tooltips = {}

# Get current directory (platforms/)
current_dir = os.path.dirname(__file__)

# Loop through each .py file in this directory
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f".{module_name}", package=__name__)

        checker_name = f"{module_name}_checker"
        if hasattr(module, checker_name):
            checker = getattr(module, checker_name)
            platform_name = module_name.capitalize()
            platform_checkers[platform_name] = checker

            # Optional: collect tooltip if defined
            if 'tooltip' in checker:
                tooltips[platform_name] = checker['tooltip']