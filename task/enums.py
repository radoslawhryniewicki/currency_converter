from enum import Enum


class Environment(Enum):
    DEV = "dev"
    PROD = "prod"


class DataSource(Enum):
    API = "api"
    JSON = "json"
