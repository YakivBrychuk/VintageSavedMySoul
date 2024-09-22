from django.core.management.base import BaseCommand
import json
from pathlib import Path

class Command(BaseCommand):
    help = "Organizes JSON data in the 'products.json' file by categories and products."

    def handle(self, *args, **kwargs):
        # Path to your input/output JSON file (same file)
        file_path = Path('products/fixtures/products.json')

        # Read the current data from the file
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON in {file_path}"))
            return

        # Organize the data
        organized_data = {"categories": [], "products": []}
        for item in data:
            if item['model'] == 'products.category':
                organized_data['categories'].append(item)
            elif item['model'] == 'products.product':
                organized_data['products'].append(item)

        # Overwrite the original file with the organized data
        try:
            with open(file_path, 'w') as f:
                json.dump(organized_data, f, indent=4)
            self.stdout.write(self.style.SUCCESS(f"Successfully organized and wrote data back to {file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to write to {file_path}: {e}"))


# Command to run in the terminal:
#python manage.py organize_json_data 
