import odmantic
from typing import Optional


class Logs(odmantic.Model):
    parser_name: Optional[str]
    action: str
    level: str
    message: str
    date: str
    entyty_id: Optional[str]