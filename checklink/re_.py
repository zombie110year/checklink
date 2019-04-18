import re

MD_LINK = re.compile(
    r"!?\[.*?\]\((?P<url>\S+)\)"
)

HTTP_URL = re.compile(
    r"(?P<protocol>https?://)(?P<domain>([^/\s]+))(?P<path>(/[^#/\s]*)+/?)?(?P<anchor>(#\S*))?"
)


def removeAnchor(match):
    """传入 HTTP_URL 的 Match 实例, 去除 anchor.
    """
    x = {
        "protocol": "",
        "domain": "",
        "path": "",
    }

    for k, v in match.groupdict().items():
        if not v is None:
            x[k] = v

    return "{protocol}{domain}{path}".format(
        **x
    )
