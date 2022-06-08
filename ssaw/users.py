from datetime import datetime
from typing import Iterator, List, Optional
from uuid import UUID

from sgqlc.operation import Operation

from .base import HQBase
from .headquarters import Client
from .headquarters_schema import HeadquartersQuery, UsersFilterInput, UsersSortInput
from .headquarters_schema import User as GraphQLUser, Viewer
from .models import InterviewerAction, User, UserRole
from .utils import filter_object, order_object


class UsersApi(HQBase):
    """ Set of functions to access and manipulate Users. """

    _apiprefix = "/api/v1"

    def __init__(self, client: Client) -> None:
        super().__init__(client)

    def get_list(self, fields: Optional[List[str]] = None,
                 order=None, skip: int = 0, take: Optional[int] = None,
                 where: Optional[UsersFilterInput] = None, **kwargs) -> Iterator[GraphQLUser]:

        if fields is None:
            fields = []
        q_args = {
        }
        if order:
            q_args["order"] = order_object(UsersSortInput, order)
        if where or kwargs:
            q_args['where'] = filter_object(UsersFilterInput, where=where, **kwargs)

        op = self._graphql_query_operation('users', q_args)
        op.users.nodes.__fields__(*fields)

        yield from self._get_full_list(op, 'users', skip=skip, take=take)

    def get_info(self, id):
        r = self._make_call(method="get", path=f"{self._url_users}/{id}")
        return r

    def get_actions_log(
            self, id: UUID, start: Optional[datetime] = None,
            end: Optional[datetime] = None) -> Iterator[InterviewerAction]:

        params = {}
        if start:
            params["start"] = start.strftime("%Y-%m-%d")
        if end:
            params["end"] = end.strftime("%Y-%m-%d")
        response = self._make_call(method="get",
                                   path=f"{self._url_interviewers}/{id}/actions-log",
                                   params=params)
        for ac in response:
            yield InterviewerAction.parse_obj(ac)

    def list_supervisors(self):
        path = self._url_supervisors
        return self._list_users(path)

    def list_interviewers(self, id):
        return self._list_users(f"{self._url_supervisors}/{id}/interviewers")

    def unarchive(self, id):
        return self._make_call(method="patch", path=f"{self._url_users}/{id}/unarchive")

    def archive(self, id):
        return self._make_call(method="patch", path=f"{self._url_users}/{id}/archive")

    def create(self, user_name: str, password: str, role: UserRole = UserRole.INTERVIEWER,
               supervisor: str = "", full_name: str = "", email: str = "", phone_number: str = "") -> None:

        user = User(user_name=user_name, password=password, role=role, supervisor=supervisor,
                    full_name=full_name, email=email, phone_number=phone_number)

        return self._make_call(method="post", path=self._url_users,
                               data=user.json(by_alias=True),
                               headers={"content-type": "application/json"})

    def viewer(self, username: Optional[str] = None, password: Optional[str] = None) -> Viewer:
        op = Operation(HeadquartersQuery)
        op.viewer()
        if username and password:
            cont = self._make_graphql_call(op, auth=(username, password))
        else:
            cont = self._make_graphql_call(op)

        return (op + cont).viewer

    def lock(self, user_name: Optional[str] = None, user_id: Optional[str] = None):
        """Lock user given either the username or guid.

        Currently only works for the admin user!
        """
        self._lock_unlock(lock=True, user_name=user_name, user_id=user_id)

    def unlock(self, user_name: Optional[str] = None, user_id: Optional[str] = None):
        """Unlock user given either the username or guid.

        Currently only works for the admin user!
        """
        self._lock_unlock(lock=False, user_name=user_name, user_id=user_id)

    def _lock_unlock(self, lock: bool, user_name: Optional[str] = None, user_id: Optional[str] = None):
        if user_name:
            try:
                user_id = next(self.get_list(fields=["id"], user_name=user_name, take=1)).id
            except StopIteration:
                raise ValueError("user_name was not found")
        if user_id:
            payload = {
                "userId": user_id,
                "isLockedByHeadquarters": lock,
                "isLockedBySupervisor": lock
            }
            return self._make_call(
                method="post",
                path=f"{self._hq.baseurl}/users/Manage",
                json=payload,
                use_login_session=True
            )
        else:
            raise ValueError("either user_name or user_id must be provided")

    def change_password(self, password: str, user_name: Optional[str] = None, user_id: Optional[str] = None):
        """Change password for a user.

        Currently only works for the admin user!
        """
        if user_name:
            try:
                user_id = next(self.get_list(fields=["id"], user_name=user_name, take=1)).id
            except StopIteration:
                raise ValueError("user_name was not found")
        if user_id:
            payload = {
                "userId": user_id,
                "password": password,
                "confirmPassword": password
            }
            return self._make_call(
                method="post",
                path=f"{self._hq.baseurl}/users/ChangePassword",
                json=payload,
                use_login_session=True
            )

    def _list_users(self, path):
        page_size = 10
        page = 1
        total_count = 11
        params = {
            'offset': page,
            'limit': page_size
        }
        while (page - 1) * page_size < total_count:
            params['offset'] = page
            r = self._make_call('get', path, params=params)
            total_count = r['TotalCount']
            if total_count > 0:
                yield from r['Users']
            else:
                yield from ()
            page += 1

    @property
    def _url_users(self):
        return f"{self.url}/users"

    @property
    def _url_supervisors(self):
        return f"{self.url}/supervisors"

    @property
    def _url_interviewers(self):
        return f"{self.url}/interviewers"
