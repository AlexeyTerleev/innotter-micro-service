from rest_framework.permissions import BasePermission
import jwt
from jwt.exceptions import InvalidTokenError

class JWTAuthentication(BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.headers.get('Authorization', '').replace("Bearer ", "")
            decoded = jwt.decode(token, 'JWT_SECRET_KEY', algorithms=['HS256'])
            access = True
        except(InvalidTokenError, jwt.ExpiredSignatureError):
            access =  False
        
        return access
    