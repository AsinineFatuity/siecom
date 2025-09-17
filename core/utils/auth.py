from jose import jwt, JWTError
import logging
import requests
from typing import Dict, Any, Union
from decouple import config
from django.core.cache import cache


class VerifyOidcToken:
    OIDC_PUBLIC_KEY_CACHE_KEY = "oidc_jwks"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.oidc_domain = config("OIDC_DOMAIN")
        self.oidc_audience = config("OIDC_AUDIENCE")
        self.jwks = self._get_oidc_json_web_key_set()
        self.decoded_data = self._decode_user_data_from_token()

    def validate_token(self) -> Union[None, Dict[str, Any]]:
        user_data = self._get_user_info_from_decoded_claims()
        return user_data

    def _get_oidc_json_web_key_set(self):
        jwks_url = f"https://{self.oidc_domain}/.well-known/jwks.json"
        jwks = cache.get(self.OIDC_PUBLIC_KEY_CACHE_KEY)
        if not jwks:
            jwks = requests.get(jwks_url).json()
            if not jwks:
                logging.error(f"{__name__}: Unable to fetch OIDC public key")
                return None
            cache.set(self.OIDC_PUBLIC_KEY_CACHE_KEY, jwks, timeout=60 * 60)
        return jwks

    def _decode_user_data_from_token(self):
        unverified_header = jwt.get_unverified_header(self.access_token)
        rsa_key = {}
        for key in self.jwks["keys"]:
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
            return None
        try:
            decoded = jwt.decode(
                self.access_token,
                rsa_key,
                algorithms=["RS256"],
                audience=self.oidc_audience,
                issuer=f"https://{self.oidc_domain}".rstrip("/"),
            )
            return decoded
        except JWTError as e:
            logging.error(f"{__name__}: Unable to decode token - {str(e)}")
        return None

    def _get_user_info_from_decoded_claims(self):
        """
        NOTE: sample decoded data looks like this
        {
            "iss": "https://dev-ayadil08ocxycfzg.us.auth0.com/",
            "sub": "google-oauth2|116335214551149049094",
            "aud": [
                "https://dev-ayadil08ocxycfzg.us.auth0.com/api/v2/",
                "https://dev-ayadil08ocxycfzg.us.auth0.com/userinfo"
            ],
            "iat": 1742339743,
            "exp": 1742426143,
            "scope": "openid profile email",
            "azp": "7muEEQsA8kcvlzgZHbLGcSYTEzFDKWdN",
        }
        """
        if not self.decoded_data:
            return None
        return {
            "oidc_id": self.decoded_data.get("sub"),
            "oidc_issuer": self.decoded_data.get("iss"),
            "email": self.decoded_data.get("email"),
            "first_name": self.decoded_data.get("given_name"),
            "last_name": self.decoded_data.get("family_name"),
            "avatar": self.decoded_data.get("picture"),
        }
