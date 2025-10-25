import os
import sys

# Add project folder to sys.path
path = "/home/chidera01/doctor_appointment_system"
if path not in sys.path:
    sys.path.append(path)

# Set Django settings
os.environ["DJANGO_SETTINGS_MODULE"] = "clinic_booking.settings"

# Activate virtualenv (for PythonAnywhere)
activate_env = "/home/chidera01/.virtualenvs/healthcare-virtualenv/bin/activate_this.py"


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
