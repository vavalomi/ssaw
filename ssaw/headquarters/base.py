import json
import re
import os
import urllib
from .exceptions import NotFoundError, NotAcceptableError
from .models import Assignment, Questionnaire

class HQBase(object):
    def __init__(self, hq):
        self._hq = hq
        self._baseurl = hq.url

    def _decode_object(self, o):
        if 'Assignments' in o:
            typestr = 'Assignments'
            ccls = Assignment
        elif 'Questionnaires' in o:
            typestr = 'Questionnaires'
            ccls = Questionnaire
        else:
            typestr = None
        
        if typestr:
            ret = []
            for item in o[typestr]:
                obj = ccls(item)
                ret.append(obj)
            return ret
        else:
            return o

    @property
    def url(self):
        return self._baseurl

    def _make_call(self, method, path, filepath = None, **kwargs):
        response = self._hq.session.request(method = method, url = path, **kwargs)
        rc = response.status_code
        if rc == 200:
            if method == 'get':
                if 'application/json' in response.headers['Content-Type']:
                    return json.loads(response.content, object_hook=self._decode_object)

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
                return True
        elif rc == 404:
            raise NotFoundError('address not found')
        elif rc == 406:
            raise NotAcceptableError(response.json()['Message'])
        else:
            response.raise_for_status
