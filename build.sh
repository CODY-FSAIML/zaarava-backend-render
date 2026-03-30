#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# NEW: Automatically create superuser using Render's environment variables
# The "|| true" prevents the build from crashing if the user already exists!
python manage.py createsuperuser --noinput || true