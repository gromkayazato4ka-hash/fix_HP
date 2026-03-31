def enforce_limit(count, limit):
    return count <= limit


def destructive_allowed(settings):
    return settings.require_confirm_destructive
