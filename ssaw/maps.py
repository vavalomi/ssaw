from typing import Generator

from sgqlc.operation import Operation

from .base import HQBase
from .exceptions import GraphQLError
from .headquarters_schema import (
    ListFilterInputTypeOfUserMapFilterInput,
    Map,
    MapsFilter,
    StringOperationFilterInput,
    UserMapFilterInput,
    headquarters_schema)


class MapsApi(HQBase):
    """ Set of functions to access and manipulate Maps. """

    def get_list(self, filter_user: str = None, fields: list = [], **kwargs) -> Generator[Map, None, None]:
        """Get list of maps

        :param filter_user: List only maps linked to the user

        :param fields: List of fields to return for each map

        :returns: List of Map objects
        """

        if filter_user:
            kwargs['users'] = ListFilterInputTypeOfUserMapFilterInput(
                some=UserMapFilterInput(
                    user_name=StringOperationFilterInput(
                        eq=filter_user)))
        maps_args = {
            'take': 20,
            'skip': 0,
        }
        if kwargs:
            maps_args['where'] = MapsFilter(**kwargs)
        filtered_count = 21
        if not fields:
            fields = [
                'file_name',
                'import_date',
            ]
        while maps_args['skip'] < filtered_count:
            op = Operation(headquarters_schema.HeadquartersQuery)
            q = op.maps(**maps_args)
            q.__fields__('filtered_count')
            q.nodes.__fields__(*fields)
            cont = self.endpoint(op)
            errors = cont.get('errors')
            if errors:
                raise GraphQLError(errors[0]['message'])
            res = (op + cont).maps

            filtered_count = res.filtered_count
            yield from res.nodes
            maps_args['skip'] += maps_args['take']

    def delete(self, file_name: str) -> Map:
        """Delete a map file

        :param file_name: Filename (with extension) to be deleted
        """
        return self._call_mutation(method_name="delete_map", file_name=file_name)

    def add_user(self, file_name: str, user_name: str) -> Map:
        """Add user-to-map link

        :param file_name: Filename of the map
        :param user_name: Interviewer role user name

        :returns: Modified Map object
        """
        return self._call_mutation(method_name="add_user_to_map", file_name=file_name, user_name=user_name)

    def delete_user(self, file_name: str, user_name: str) -> Map:
        """Remove user-to-map link

        :param file_name: Filename of the map
        :param user_name: Interviewer role user name

        :returns: Modified Map object
        """
        return self._call_mutation(method_name="delete_user_from_map", file_name=file_name, user_name=user_name)

    def _call_mutation(self, method_name: str, fields: list = [], **kwargs) -> Map:
        if not fields:
            fields = [
                'file_name',
                'import_date',
            ]
        op = Operation(headquarters_schema.HeadquartersMutation)
        func = getattr(op, method_name)
        func(**kwargs).__fields__(*fields)
        cont = self.endpoint(op)
        errors = cont.get('errors')
        if errors:
            raise GraphQLError(errors[0]['message'])
        res = (op + cont)
        return getattr(res, method_name)
