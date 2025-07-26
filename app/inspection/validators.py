import re
from urllib.parse import urlparse


def validate_image_url(image_url):
    """Validate that image URL ends with allowed image extensions"""
    if not image_url:
        return False
    
    try:
        # Parse the URL to get the path
        parsed_url = urlparse(image_url)
        
        # Get the file extension
        path = parsed_url.path.lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        
        return any(path.endswith(ext) for ext in allowed_extensions)
    
    except Exception:
        return False
    

def validate_vehicle_number(vehicle_number):
    """Validate vehicle number format (basic validation)"""
    
    if len(vehicle_number) < 5 or len(vehicle_number) > 20:
        return False, "Vehicle number must be between 5 and 20 characters"
    
    # Remove spaces and check if it contains only alphanumeric characters
    cleaned = vehicle_number.replace(' ', '')
    if not re.match(r'^[a-zA-Z0-9]+$', cleaned):
        return False, "Vehicle number can only contain letters and numbers"
    
    return True, "Vehicle number is valid"