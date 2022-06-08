import json
import ntpath
from typing import Iterator, List, Optional

from sgqlc.operation import Operation
from sgqlc.types import Arg, Variable, non_null

from .base import HQBase
from .exceptions import GraphQLError, NotAcceptableError, UnauthorizedError
from .headquarters_schema import (
    HeadquartersMutation,
    HeadquartersQuery,
    ListFilterInputTypeOfUserMapFilterInput,
    Map,
    MapsFilter,
    MapsSort,
    StringOperationFilterInput,
    Upload,
    UserMapFilterInput
)
from .models import Version
from .utils import order_object


class MapsApi(HQBase):
    """ Set of functions to access and manipulate Maps. """

    def get_list(self, filter_user: Optional[str] = None, fields: Optional[List[str]] = None,
                 order: Optional[list] = None, skip: Optional[int] = None,
                 take: Optional[int] = None, **kwargs) -> Iterator[Map]:
        """Get list of maps

        :param filter_user: List only maps linked to the user

        :param fields: List of fields to return for each map

        :returns: List of Map objects
        """

        if filter_user:
            kwargs["users"] = ListFilterInputTypeOfUserMapFilterInput(
                some=UserMapFilterInput(
                    user_name=StringOperationFilterInput(
                        eq=filter_user)))
        maps_args = {
            "workspace": self.workspace
        }
        if kwargs:
            maps_args["where"] = MapsFilter(**kwargs)
        if order:
            maps_args["order"] = order_object(MapsSort, order)
        if skip:
            maps_args["skip"] = skip
        if take:
            maps_args["take"] = take

        if not fields:
            fields = self._default_fields()

        op = Operation(HeadquartersQuery)
        q = op.maps(**maps_args)
        q.__fields__('filtered_count')
        q.nodes.__fields__(*fields)

        cont = self._make_graphql_call(op)
        res = (op + cont).maps

        yield from res.nodes

    def delete(self, file_name: str) -> Map:
        """Delete a map file

        :param file_name: Filename (with extension) to be deleted
        """
        return self._call_mutation(method_name="delete_map",
                                   file_name=file_name,
                                   fields=self._default_fields())

    def upload(self, zip_file, fields: Optional[List[str]] = None) -> bool:
        """Upload a zip file with maps.
        For versions before 22.06 only works for the admin user!

        :param zip_file: Archive with the maps

        :returns: `True` if successful, otherwise raises `GraphQLError` or `NotAcceptableError`
        """
        files = {"file": (ntpath.basename(zip_file), open(zip_file, 'rb'), 'application/zip')}

        if self._hq.version < Version("22.06 (build 33000)"):
            ret = self._make_call(method="post",
                                  path=f"{self.url}api/MapsApi/Upload",
                                  files=files,
                                  use_login_session=True)

        else:
            if not fields:
                fields = self._default_fields()
            op = Operation(HeadquartersMutation, variables={'file': Arg(non_null(Upload)), })
            op.upload_map(file=Variable('file')).__fields__(*fields)

            operations = {
                "query": bytes(op).decode('utf-8'),
                "variables": {"file": None},
            }

            data = {
                "operations": json.dumps(operations),
                "map": '{ "file": ["variables.file"] }',
            }
            cont = self._make_call(method="post",
                                   path=f"{self._hq.baseurl}/graphql",
                                   data=data,
                                   files=files)

            errors = cont.get("errors")

            if not errors:

                ret = (op + cont)
                return ret.upload_map

            try:
                rc = errors[0]['extensions']['code']
            except KeyError:
                rc = None
            if rc == 'AUTH_NOT_AUTHENTICATED':
                raise UnauthorizedError()
            else:
                raise GraphQLError(errors[0]['message'])

        if ret["isSuccess"]:
            return True
        else:
            raise NotAcceptableError(ret["errors"][0])

    def add_user(self, file_name: str, user_name: str) -> Map:
        """Add user-to-map link

        :param file_name: Filename of the map
        :param user_name: Interviewer role user name

        :returns: Modified Map object
        """
        return self._call_mutation(method_name="add_user_to_map",
                                   file_name=file_name, user_name=user_name,
                                   fields=self._default_fields())

    def delete_user(self, file_name: str, user_name: str) -> Map:
        """Remove user-to-map link

        :param file_name: Filename of the map
        :param user_name: Interviewer role user name

        :returns: Modified Map object
        """
        return self._call_mutation(method_name="delete_user_from_map",
                                   file_name=file_name,
                                   user_name=user_name,
                                   fields=self._default_fields())

    def _default_fields(self):
        if self._hq.version < Version("21.05 (build 31160)"):
            return [
                "file_name",
                "import_date",
            ]
        else:
            return [
                "file_name",
                "import_date_utc",
            ]
