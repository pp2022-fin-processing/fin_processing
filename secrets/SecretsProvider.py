import json
from pathlib import Path

VAULT_FILE_NAME = 'vault.json'
API_FILE_NAME = 'apis.json'
API_KEY_ATTRIBUTE = 'api_key'


class KeyNotProvided(Exception):
    pass


class SecretProvider:
    def __init__(self):
        vault_file = Path(VAULT_FILE_NAME)
        if not vault_file.is_file():
            vault_dict = {
                'alpha_vantage': {
                    'api_key': ''
                },
                'twelve_data': {
                    'api_key': ''
                },
                'rapid_api': {
                    'api_key': ''
                }
            }
            vault_json = json.dumps(vault_dict, indent=4)
            vault_file = open(VAULT_FILE_NAME, 'w')
            vault_file.write(vault_json)

    def get_api_credentials(self, api_name):
        vault_file = open(VAULT_FILE_NAME)
        vault_dict = json.loads(vault_file.read())
        if vault_dict[api_name][API_KEY_ATTRIBUTE] == '':
            raise KeyNotProvided(f'In order to use {api_name} API, proper key is required.'
                                 f' Please provide it to secrets/\'{VAULT_FILE_NAME}\' file.')
        else:
            api_file = open(API_FILE_NAME, 'r')
            api_dict = json.loads(api_file.read())
            api_dict[api_name][API_KEY_ATTRIBUTE] = vault_dict[api_name][API_KEY_ATTRIBUTE]
            return api_dict[api_name]


secret_provider = SecretProvider()
print(secret_provider.get_api_credentials('twelve_data')['api_key'])
