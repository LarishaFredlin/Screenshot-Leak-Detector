
import re
import config


def check_keywords(text):
    detected = []
    normalized_text = re.sub(r"\s+", " ", text.lower()).strip()

    for keyword in config.SENSITIVE_KEYWORDS:
        normalized_keyword = re.sub(
            r"\s+", " ", keyword.lower()
        ).strip()

        # Match the complete keyword, not part of a larger word.
        pattern = (
            r"(?<!\w)"
            + re.escape(normalized_keyword)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_text):
            detected.append(keyword)

    return detected

