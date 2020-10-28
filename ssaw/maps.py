from typing import Generator

from sgqlc.operation import Operation

from .base import HQBase
from .exceptions import GraphQLError
from .headquarters_schema import Map, MapsFilter, UserMapFilter, headquarters_schema


class MapsApi(HQBase):
    def get_list(self, filter_user: str = None, fields: list = [], **kwargs) -> Generator[Map, None, None]:
        """Get list of maps

        Parameters
        ----------
        filter_user : str, optional
            List only maps linked to the user

        fields : list, optional
            List of fields to return for each map

        Yields
        -------
        list of :class:`ssaw.headquarters_schema.Map` objects
        """

        if filter_user:
            kwargs['users_some'] = UserMapFilter(user_name=filter_user)
        where = MapsFilter(**kwargs)
        take = 20
        skip = 0
        filtered_count = 21
        if not fields:
            fields = [
                'file_name',
                'import_date',
            ]
        while skip < filtered_count:
            op = Operation(headquarters_schema.HeadquartersQuery)
            q = op.maps(take=take, skip=skip, where=where)
            q.__fields__('filtered_count')
            q.nodes.__fields__(*fields)
            cont = self.endpoint(op)
            errors = cont.get('errors')
            if errors:
                raise GraphQLError(errors[0]['message'])
            res = (op + cont).maps

            filtered_count = res.filtered_count
            yield from res.nodes
            skip += take

    def delete(self, file_name: str) -> Map:
        """Delete a map file

        Parameters
        ----------
        file_name : str
            Filename (with extension) to be deleted
        """
        return self._call_mutation(method_name="delete_map", file_name=file_name)

    def add_user(self, file_name: str, user_name: str) -> Map:
        """Add user-to-map link

        Parameters
        ----------
        file_name : str
            Filename of the map

        user_name: str
            Interviewer role user name

        Yields
        -------
        Modified :class:`ssaw.headquarters_schema.Map` object
        """
        return self._call_mutation(method_name="add_user_to_map", file_name=file_name, user_name=user_name)

    def delete_user(self, file_name: str, user_name: str) -> Map:
        """Remove user-to-map link

        Parameters
        ----------
        file_name : str
            Filename of the map

        user_name: str
            Interviewer role user name

        Yields
        -------
        Modified :class:`ssaw.headquarters_schema.Map` object
        """
        return self._call_mutation(method_name="delete_user_from_map", file_name=file_name, user_name=user_name)

    def _call_mutation(self, method_name: str, fields: list = [], **kwargs) -> Map:
        if not fields:
            fields = [
                'file_name',
                'import_date',
            ]
        op = Operation(headquarters_schema.HeadquartersMutations)
        func = getattr(op, method_name)
        func(**kwargs).__fields__(*fields)
        cont = self.endpoint(op)
        errors = cont.get('errors')
        if errors:
            raise GraphQLError(errors[0]['message'])
        res = (op + cont)
        return getattr(res, method_name)
