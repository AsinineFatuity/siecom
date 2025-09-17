from jose import jwt, JWTError
import logging
import requests
from typing import Dict, Any
from decouple import config
from django.core.cache import cache


class VerifyOidcToken:
    OIDC_PUBLIC_KEY_CACHE_KEY = "oidc_jwks"
    OIDC_USERINFO_CACHE_KEY = "oidc_userinfo"

    def __init__(self, oidc_token: str):
        self._oidc_access_token = oidc_token
        self._oidc_domain = config("OIDC_DOMAIN")
        self._oidc_audience = config("OIDC_AUDIENCE")
        self._jwks = self._get_oidc_json_web_key_set()
        self._decoded_data = self._decode_user_data_from_token()

    def verify_token(self) -> Dict[str, Any]:
        user_data = self._get_user_info_from_decoded_claims()
        return user_data

    def _get_oidc_json_web_key_set(self):
        jwks_url = f"https://{self._oidc_domain}/.well-known/jwks.json"
        jwks = cache.get(self.OIDC_PUBLIC_KEY_CACHE_KEY)
        if not jwks:
            jwks = requests.get(jwks_url).json()
            if not jwks:
                logging.error(f"{__name__}: Unable to fetch OIDC public key")
                return None
            cache.set(self.OIDC_PUBLIC_KEY_CACHE_KEY, jwks, timeout=60 * 60)
        return jwks

    def _get_user_info_endpoint(self):
        well_known_url = f"https://{self._oidc_domain}/.well-known/openid-configuration"
        info_response = cache.get(self.OIDC_USERINFO_CACHE_KEY)
        if not info_response:
            response = requests.get(well_known_url)
            if response.status_code == 200:
                config_data = response.json()
                info_response = config_data.get("userinfo_endpoint")
                cache.set(self.OIDC_USERINFO_CACHE_KEY, info_response, timeout=60 * 60)
            else:
                logging.error(f"{__name__}: Unable to fetch OIDC configuration")
        return info_response

    def _decode_user_data_from_token(self):
        unverified_header = jwt.get_unverified_header(self._oidc_access_token)
        rsa_key = {}
        decoded_data = {}
        for key in self._jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break
        if not rsa_key:
            logging.error(
                f"{__name__}: Unable to find OIDC provider public key to verify token"
            )
            return decoded_data
        try:
            decoded_data = jwt.decode(
                self._oidc_access_token,
                rsa_key,
                algorithms=["RS256"],
                audience=self._oidc_audience,
                issuer=f"https://{self._oidc_domain}".rstrip("/"),
            )
        except JWTError as e:
            logging.error(f"{__name__}: Unable to decode token - {str(e)}")
        return decoded_data

    def _request_user_info_from_oidc_provider(self):
        userinfo_url = self._get_user_info_endpoint()
        user_info = {}
        if not userinfo_url:
            return user_info
        headers = {"Authorization": f"Bearer {self._oidc_access_token}"}
        response = requests.get(userinfo_url, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
        return user_info

    def _get_user_info_from_decoded_claims(self):
        """
        NOTE: sample decoded data looks like this (Auth0 OIDC provider example)
        {
            "iss": "https://dev-myown-domain.us.auth0.com/",
            "sub": "google-oauth2|116335214551149049094",
            "aud": [
                "https://dev-myown-domain.us.auth0.com/api/v2/",
                "https://dev-myown-domain.us.auth0.com/userinfo"
            ],
            "iat": 1742339743,
            "exp": 1742426143,
            "scope": "openid profile email",
            "azp": "7muEEQsA8kcvlzgZHbLGcSYTEzFDKWdN",
        }
        """
        if not self._decoded_data:
            return {}
        user_info = self._request_user_info_from_oidc_provider()
        return {
            "oidc_subject": self._decoded_data.get("sub"),
            "oidc_issuer": self._decoded_data.get("iss"),
            "email": user_info.get("email"),
            "first_name": user_info.get("given_name", "Anon"),
            "last_name": user_info.get("family_name", "User"),
        }
