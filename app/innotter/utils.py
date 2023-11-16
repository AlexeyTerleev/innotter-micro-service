import jwt


def get_user_info(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    decoded = jwt.decode(token, "JWT_SECRET_KEY", algorithms=["HS256"])
    user_info = decoded.get("sub", {})
    return user_info
