#!/bin/bash
# AgriWealth Setup Script

echo "=== AgriWealth Setup ==="

# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
if [ ! -f .env ]; then
cat > .env << EOF
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your-openai-api-key-here
EOF
echo ".env file created. Please update OPENAI_API_KEY if you want full AI chatbot."
fi

# 4. Run migrations
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations marketplace
python manage.py makemigrations chat
python manage.py makemigrations chatbot
python manage.py migrate

# 5. Create superuser prompt
echo ""
echo "Create an admin superuser:"
python manage.py createsuperuser

# 6. Load sample data
python manage.py shell << PYEOF
from accounts.models import User
from marketplace.models import WasteCategory

categories = [
    ('Crop Residues', 'crop-residues', 'Rice straw, wheat straw, sugarcane bagasse', '🌾'),
    ('Animal Manure', 'animal-manure', 'Cow dung, poultry waste, pig manure', '🐄'),
    ('Vegetable Waste', 'vegetable-waste', 'Spoiled or surplus vegetables and fruits', '🥦'),
    ('Husk & Shells', 'husk-shells', 'Rice husk, groundnut shells, coconut shells', '🥥'),
    ('Forestry Waste', 'forestry-waste', 'Sawdust, wood chips, bark', '🪵'),
    ('Oilseed Cake', 'oilseed-cake', 'Neem cake, groundnut cake, mustard cake', '🌻'),
]

for name, slug, desc, icon in categories:
    WasteCategory.objects.get_or_create(
        slug=slug, defaults={'name': name, 'description': desc, 'icon': icon}
    )
print("Sample categories created!")
PYEOF

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Start the development server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Admin panel: http://127.0.0.1:8000/admin/"
echo "Homepage:    http://127.0.0.1:8000/"
