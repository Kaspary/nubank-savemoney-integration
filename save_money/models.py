from datetime import date
from dataclasses import dataclass
from typing import List

@dataclass
class UserAuth:
    username: str
    password: str


@dataclass
class Token:
    access_token: str
    refresh_token: str


@dataclass
class Category:
    id: int
    name: str
    is_expense: bool
    is_default: bool
    category_type: str


@dataclass
class Movimentation:
    is_expense: bool
    title: str
    value: float
    description: str = ''
    category: Category = None
    number_of_installments: int = 1
    efetivation_date: date = date.today()
    tags: List[str] = None
