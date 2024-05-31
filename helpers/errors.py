from schemas import HTTPError, Property


responses_get_property_list = {
    200: {"model": Property},
    400: {
        "model": HTTPError,
    }
},
