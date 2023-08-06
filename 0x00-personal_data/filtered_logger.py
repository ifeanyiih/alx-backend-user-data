#!/usr/bin/env python3
"""This module further solidifies the concepts
of Personally Identifiable information (PII),
How to implement a log filter that will obfuscate PII fields
How to encrypt a password and check the validity of an input
password
How to authenticate to a database using environment variables"""
import re
import typing


def filter_datum(fields: typing.List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns a message in
    obfuscated form"""
    for field in fields:
        regex: str = r'({}=)(.+?)({})'.format(field, separator)
        message: str = re.sub(regex, r'\1' + redaction + r'\3', message)
    return message
