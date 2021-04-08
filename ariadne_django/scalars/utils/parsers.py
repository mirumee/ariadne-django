from datetime import datetime
from typing import Any, List, Optional

import dateutil.parser


def parse_value(value: Any, formats: List[str]) -> Optional[datetime]:
    for format_str in formats:
        try:
            return datetime.strptime(value, format_str)
        except (ValueError, TypeError):
            continue

    # fallback to using dateutil parser
    try:
        return dateutil.parser.parse(value)
    except (ValueError, TypeError):
        return None
