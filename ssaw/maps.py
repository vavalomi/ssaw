from typing import Generator

from sgqlc.operation import Operation

from .base import HQBase
from .exceptions import NotAcceptableError
from .headquarters_schema import (
    HeadquartersQuery,
    ListFilterInputTypeOfUserMapFilterInput,
    Map,
    MapsFilter,
    StringOperationFilterInput,
    UserMapFilterInput
)
from .models import Version
from .utils import order_object


class MapsApi(HQBase):
    """ Set of functions to access and manipulate Maps. """

    def get_list(self, filter_user: str = None, fields: list = [],
                 order: list = None, skip: int = None, take: int = None, **kwargs) -> Generator[Map, None, None]:
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
            maps_args["order"] = order_object("MapsSort", order)
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

    def upload(self, zip_file) -> bool:
        """Upload a zip file with maps
        Currently only works for the admin user!

        :param file_name: Archive with extension with the maps

        :returns: `True` if successful, otherwise raises `NotAcceptableError`
        """
        ret = self._make_call(method="post", path=f"{self.url}/api/MapsApi/Upload",
                              files={'file': open(zip_file, 'rb')}, use_login_session=True)
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
