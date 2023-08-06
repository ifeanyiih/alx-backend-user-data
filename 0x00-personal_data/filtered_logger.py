#!/usr/bin/env python3
"""This module further solidifies the concepts
of Personally Identifiable information (PII),
How to implement a log filter that will obfuscate PII fields
How to encrypt a password and check the validity of an input
password
How to authenticate to a database using environment variables"""
import re
import typing
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: typing.List[str]) -> None:
        """Initializes the Class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """method to filter values in incoming log records using
        filter_datum"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: typing.List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns a message in
    obfuscated form"""
    for field in fields:
        regex: str = r'({}=)(.+?)({})'.format(field, separator)
        message: str = re.sub(regex, r'\1' + redaction + r'\3', message)
    return message
