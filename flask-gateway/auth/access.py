import requests, os
"""
Connect to auth service
Login and get token
Validate token
"""

def login(username,password):
    """
    Get username and password
    Get authenticated by auth service
    Return token for valid credentials
    Return error for invalid credentials
    """

    response = requests.post(f"{os.environ.get('AUTH_SVC_URL')}/login",auth=(username,password))

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text,response.status_code)
    
def validate_jwt(request):
    """
    Get request object
    Get token from Authorization header
    validate token by auth service
    Return details for valid token
    Return error for invalid token
    """
    # Check authorization header
    if "Authorization" in request.headers:
        auth_token = request.headers["Authorization"]
        # post auth service
        response = requests.post(f"{os.environ.get('AUTH_SVC_URL')}/validate", headers={"Authorization": auth_token})
        if response.status_code == 200:
            return response.text, None
        else:
            return None, (response.text,response.status_code)
    else:
        return None, ("Missing Authorization header",401)