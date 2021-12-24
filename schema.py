USER_CREATE = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string"
        },
        "email": {
            "type": "string",
        },
        "password": {
            "type": "string",
        }
    },
    "required": ["username", "email", "password"]
}

ADS_CREATE = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "descriptions": {
            "type": "string"
        },
        "owner": {
            "type": "integer"
        }


    },
    "required": ["name", "descriptions", "owner"]
}
