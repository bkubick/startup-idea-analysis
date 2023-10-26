# coding: utf-8

from __future__ import annotations

from dataclasses import dataclass
import typing


@dataclass
class Company:
    """ Company dataclass

        Attributes:
            name (str): Company name
            description (str): Company description
            size (int): Company size
            location (str): Company location
            industries (List[str]): Company industries
            url (str): Company url
    """
    name: str
    description: str
    size: int
    location: str
    industries: typing.List[str]
    url: str
