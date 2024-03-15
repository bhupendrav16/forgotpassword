class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            if not old_password or not new_password:
                return Response(
                    {
                        "status": False,
                        "status_code": 400,
                        "message": "Old password and new password are required fields.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not user.check_password(old_password):
                return Response(
                    {
                        "status": False,
                        "status_code": 401,
                        "message": "Old password is incorrect.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
                
            user.set_password(new_password)
            user.save()

            return Response({
                "status": True,
                "message": "Password updated successfully.",
            })

        except Exception as err:
            return Response(
                {
                    "status": False,
                    "status_code": 500,
                    "message": "Something went wrong",
                    "error": str(err),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
