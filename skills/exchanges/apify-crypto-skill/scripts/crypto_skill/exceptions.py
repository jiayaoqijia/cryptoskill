class CryptoSkillError(Exception):
    """Base exception for all crypto skill errors."""


class ApifyAuthError(CryptoSkillError):
    """Missing or invalid APIFY_API_TOKEN (401/403)."""


class ApifyActorError(CryptoSkillError):
    """Actor run failed: non-2xx status, rate limit (429), or connection error."""


class ApifyTimeoutError(CryptoSkillError):
    """Actor run exceeded timeout (408 or httpx timeout)."""


class ActorDataError(CryptoSkillError):
    """Actor response doesn't match expected schema."""
