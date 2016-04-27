import requests

def _perform_request(url, method, params={}, headers={}, paginated=True, json=True):
    '''
    Perform an HTTP request.
    '''
    func = getattr(requests, method)

    # perform paginated requests
    params.update({"per_page": 100})
    result = func(url, params=params, headers=headers)

    if not paginated:
        if result.status_code in [200, 201]:
            if json:
                return result.json()
            else:
                return result
        else:
            raise Exception("Failed request {}".format(result.status_code))

    # paginated request
    final_results = []
    final_results.extend(result.json())
    while "link" in result.headers:
        url_parts = result.headers["link"].split()
        if url_parts[1] != 'rel="next",':
            break
        else:
            next_url = url_parts[0].strip("<").rstrip(">;")
            result = func(next_url, headers=headers)
            final_results.extend(result.json())

    return final_results

