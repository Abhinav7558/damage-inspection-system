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