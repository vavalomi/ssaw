from typing import Iterator, List, Optional

from .base import HQBase
from .exceptions import FeatureNotSupported
from .headquarters import Client
from .models import Version, Workspace, WorkspaceStatus, WorkspacesList
from .utils import fix_qid


class WorkspacesApi(HQBase):
    """ Set of functions to access and manipulate Workspaces. """

    _apiprefix = "/api/v1/workspaces"

    def __init__(self, client: Client):
        if client.version < Version("21.01 (build 30293)"):
            raise FeatureNotSupported

        super().__init__(client)

    @fix_qid(expects={'user_id': 'string'})
    def get_list(self, user_id: Optional[str] = None, include_disabled: bool = False) -> Iterator[Workspace]:
        path = self.url
        length = 10
        start = 0
        total_count = 11
        params = {
            'start': start,
            'length': length,
            'IncludeDisabled': include_disabled,
            'UserId': user_id
        }
        while start < total_count:
            params['start'] = start
            r = WorkspacesList.parse_obj(self._make_call('get', path, params=params))
            if r.total_count:
                total_count = r.total_count
                yield from r.workspaces
            else:
                yield from ()
            start += length

    def get_info(self, name: str) -> Workspace:
        return Workspace.parse_obj(self._make_call(method="get", path=f"{self.url}/{name}"))

    def create(self, name: str, display_name: str) -> Workspace:
        return Workspace.parse_obj(
            self._make_call(method="post",
                            path=self.url,
                            json={'Name': name, 'DisplayName': display_name}))

    def update(self, name: str, display_name: str):
        _ = self._make_call(method="patch",
                            path=f"{self.url}/{name}",
                            json={'DisplayName': display_name})

    def delete(self, name: str):
        _ = self._make_call(method="delete", path=f"{self.url}/{name}")

    def enable(self, name: str):
        _ = self._make_call(method="post", path=f"{self.url}/{name}/enable")

    def disable(self, name: str):
        _ = self._make_call(method="post", path=f"{self.url}/{name}/disable")

    def assign(self, user_ids: List[str], workspaces: List[str],
               supervisors: Optional[List[str]] = None, mode: str = "add"):

        if not isinstance(user_ids, list):
            user_ids = [user_ids]
        if not isinstance(workspaces, list):
            workspaces = [workspaces]
        if not isinstance(supervisors, list):
            supervisors = [supervisors]
        if mode.lower() not in ["add", "assign", "remove"]:
            raise ValueError("mode parameter must be one of 'add', 'assign', or 'remove'")

        data = {
            "UserIds": user_ids,
            "Workspaces": [{"workspace": w, "supervisorId": s} for w, s in zip(workspaces, supervisors)],
            "Mode": mode
        }
        _ = self._make_call(method="post", path=f"{self.url}/assign", json=data)

    def status(self, name: str) -> WorkspaceStatus:
        return WorkspaceStatus.parse_obj(self._make_call(method="get", path=f"{self.url}/status/{name}"))
