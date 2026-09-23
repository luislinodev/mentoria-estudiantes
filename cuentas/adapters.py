from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AdaptadorSocial(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.first_name = data.get("given_name") or data.get("first_name") or user.first_name
        user.last_name = data.get("family_name") or data.get("last_name") or user.last_name
        return user
