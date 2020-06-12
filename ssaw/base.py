import json
import re
import os
from .exceptions import NotFoundError, NotAcceptableError
from sgqlc.endpoint.requests import RequestsEndpoint


class HQBase(object):
    _apiprefix = ""

    def __init__(self, client):
        self._hq = client
        self.endpoint = RequestsEndpoint(client.baseurl +'/graphql', session=client.session)

    @property
    def url(self):
        return self._hq.baseurl + self._apiprefix

    def _make_call(self, method, path, filepath = None, parser=None, **kwargs):
        response = self._hq.session.request(method = method, url = path, **kwargs)
        rc = response.status_code
        if rc < 300:
            if method == 'get':
                if 'application/json' in response.headers['Content-Type']:
                    if parser:
                        return parser(response.content)
                    else:
                        return json.loads(response.content)

                elif 'application/zip' in response.headers['Content-Type']:
                    d = response.headers['content-disposition']
                    fname = re.findall(r"filename[ ]*=([^;]+)", d, flags=re.IGNORECASE)

                    if not fname:
                        fname = re.findall(r"filename\*=utf-8''(.+)", d, flags=re.IGNORECASE)
                    fname = fname[0].strip().strip('"')
                    outfile = os.path.join(filepath, fname)

                    with open(outfile, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024): 
                            if chunk:
                                f.write(chunk)
                    return outfile
                else:
                    return response.content
            else:
                if response.content:
                    return json.loads(response.content)
                else:
                    return True
        elif rc == 404:
            raise NotFoundError(response.text)
        elif rc == 406:
            raise NotAcceptableError(response.text)
        else:
            response.raise_for_status()
