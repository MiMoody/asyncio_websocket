import urllib.parse as urlparse

def get_params_url(url:str):
    parsed_query = urlparse.urlparse(url).query
    params = urlparse.parse_qs(parsed_query)
    return params

def set_params_url(url:str, params:dict):
    url_parse = urlparse.urlparse(url)
    query = url_parse.query
    url_dict = dict(urlparse.parse_qsl(query))
    url_dict.update(params)
    url_new_query = urlparse.urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    new_url = urlparse.urlunparse(url_parse)
    print(new_url)
    return new_url