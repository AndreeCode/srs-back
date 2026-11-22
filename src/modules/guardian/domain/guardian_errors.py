class GuardianValidationError(ValueError):
    pass


class GuardianConflictError(ValueError):
    pass


class GuardianChildNotFoundError(ValueError):
    pass


class GuardianLinkRateLimitError(ValueError):
    pass
