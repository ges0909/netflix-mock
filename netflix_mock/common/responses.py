_content = {
    "application/json": {
        # "properties": [
        #     {
        #         "detail": {
        #             "type": "string",
        #         },
        #     }
        # ],
        "example": {
            "detail": "string",
        },
    },
}

HTTP_401_UNAUTHORIZED = {
    401: {
        "description": "Unauthorized",
        "content": {**_content},
    },
}

HTTP_404_NOT_FOUND = {
    404: {
        "description": "Not Found",
        "content": {**_content},
    },
}


HTTP_409_CONFLICT = {
    409: {
        "description": "Conflict",
        "content": {**_content},
    },
}

HTTP_500_INTERNAL_SERVER_ERROR = {
    500: {
        "description": "Internal Server Error",
        "content": {**_content},
    },
}
