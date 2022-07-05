import os
from robot.libraries.BuiltIn import BuiltIn
from RPA.Robocorp.Vault import Vault
from Communicate import CustomVault


def log_to_console(message: str) -> None:

    BuiltIn().log_to_console(f"\n{message}")


def is_local():
    try:
        return os.environ["ENVIRONMENT"] == "LOCAL"
    except:
        return False


def is_dev():
    try:
        return os.environ["ENVIRONMENT"] == "DEV"
    except:
        return False


def is_our_uat():
    try:
        return os.environ["ENVIRONMENT"] == "OUR_UAT"
    except:
        return False


def is_client_uat():
    try:
        return os.environ["ENVIRONMENT"] == "UAT"
    except:
        return False


def is_production():
    try:
        return os.environ["ENVIRONMENT"] == "PRODUCTION"
    except:
        return False


def get_vault(vault_name):
    if(is_local()):
        vault = Vault()
        secret = vault.get_secret(vault_name)
    else:
        secret = CustomVault(identifier=get_identifier(),
                             URL=get_base_url()).get_vault(vault_name)

    return secret


def get_identifier():

    try:
        if os.environ["LOCAL_TO_DEV_SERVER"] == "True":
            return "d847ffb1-a803-4ede-ab57-f44776257b69"
    except:
        pass

    identifier = BuiltIn().get_variable_value("${identifier}")
    return identifier


def get_base_url():
    try:
        if os.environ["LOCAL_TO_DEV_SERVER"] == "True":
            return "http://13.58.117.7:8000/api/v1"
    except:
        pass

    if is_local():
        return "http://localhost:8000/api/v1"

    elif is_dev():
        return "http://13.58.117.7:8000/api/v1"

    elif is_our_uat():
        return "http://18.224.145.213:8000/api/v1"

    elif is_client_uat():
        return "<client_uat_url>:8000/api/v1"

    elif is_production():
        return "<production_url>:8000/api/v1"

    else:
        return "http://localhost:8000/api/v1"
