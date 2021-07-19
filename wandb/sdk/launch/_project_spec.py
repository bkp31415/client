"""Internal utilities for parsing MLproject YAML files."""

import json
import logging
import os
from shlex import quote
import tempfile
from typing import Tuple

import wandb
from wandb.errors import Error as ExecutionException
from wandb.sdk.lib.runid import generate_id

from . import utils

if wandb.TYPE_CHECKING:
    from wandb.apis.internal import Api
    from typing import Any, Dict, List, Optional


_logger = logging.getLogger(__name__)

MLPROJECT_FILE_NAME = "mlproject"
DEFAULT_CONFIG_PATH = "launch_override_config.json"


class Project(object):
    """A launch project specification."""

    def __init__(
        self,
        uri: str,
        target_entity: str,
        target_project: str,
        name: str,
        docker_config: Dict[str, Any],
        git_info: Dict[str, str],
        overrides: Dict[str, Any],
    ):

        self.uri = uri
        self.target_entity = target_entity
        self.target_project = target_project
        self.name = name
        self.docker_image: Optional[str] = docker_config.get("docker_image")
        self.docker_user_id: int = docker_config.get("user_id", 1000)
        self.git_version: Optional[str] = git_info.get("version")
        self.git_repo: Optional[str] = git_info.get("repo")
        self.override_args: Dict[str, Any] = overrides.get("args", {})
        self.override_config: Dict[str, Any] = overrides.get("run_config", {})
        self._entry_points: Dict[
            str, EntryPoint
        ] = {}  # todo: keep multiple entrypoint support?
        if "entry_point" in overrides:
            self.add_entry_point(overrides["entry_point"])

        self.run_id = generate_id()
        self.dir = tempfile.mkdtemp()
        self.config_path = DEFAULT_CONFIG_PATH

        self.clear_parameter_run_config_collisions()

    def clear_parameter_run_config_collisions(self) -> None:
        if not self.override_config:
            return
        keys = [key for key in self.override_config.keys()]
        for key in keys:
            if self.override_args.get(key):
                del self.override_config[key]

    def get_single_entry_point(self) -> "EntryPoint":
        # assuming project only has 1 entry point, pull that out
        # tmp fn until we figure out if we wanna support multiple entry points or not
        if len(self._entry_points) != 1:
            raise Exception("Project must have exactly one entry point")
        return list(self._entry_points.values())[0]

    def add_entry_point(self, entry_point: str) -> "EntryPoint":
        _, file_extension = os.path.splitext(entry_point)
        ext_to_cmd = {".py": "python", ".sh": os.environ.get("SHELL", "bash")}
        if file_extension in ext_to_cmd:
            command = "%s %s" % (ext_to_cmd[file_extension], quote(entry_point))
            new_entrypoint = EntryPoint(name=entry_point, command=command)
            self._entry_points[entry_point] = new_entrypoint
            return new_entrypoint
        raise ExecutionException(
            "Could not find {0} among entry points {1} or interpret {0} as a "
            "runnable script. Supported script file extensions: "
            "{2}".format(
                entry_point, list(self._entry_points.keys()), list(ext_to_cmd.keys())
            )
        )

    def get_entry_point(self, entry_point: str) -> "EntryPoint":
        if entry_point in self._entry_points:
            return self._entry_points[entry_point]
        return self.add_entry_point(entry_point)

    def _fetch_project_local(self, api: Api) -> None:
        """
        Fetch a project into a local directory, returning the path to the local project directory.
        """
        parsed_uri = self.uri
        if utils._is_wandb_uri(self.uri):
            run_info = utils.fetch_wandb_project_run_info(self.uri, api)
            if not run_info["git"]:
                raise ExecutionException("Run must have git repo associated")
            utils._fetch_git_repo(
                self.dir, run_info["git"]["remote"], run_info["git"]["commit"]
            )
            patch = utils.fetch_project_diff(self.uri, api)
            if patch:
                utils.apply_patch(patch, self.dir)

            if not self._entry_points:
                self.add_entry_point(run_info["program"])  # @@@

            self.override_args = utils.merge_parameters(
                self.override_args, run_info["args"]
            )
        else:
            assert utils._GIT_URI_REGEX.match(parsed_uri), (
                "Non-wandb URI %s should be a Git URI" % parsed_uri
            )

            if not self._entry_points:
                wandb.termlog(
                    "Entry point for repo not specified, defaulting to main.py"
                )
                self.add_entry_point("main.py")

            utils._fetch_git_repo(self.dir, parsed_uri, self.git_version)

    def _copy_config_local(self) -> None:
        if not self.override_config:
            return None
        with open(os.path.join(self.dir, DEFAULT_CONFIG_PATH), "w+") as f:
            json.dump(self.override_config, f)


class EntryPoint(object):
    """An entry point into a wandb launch specification."""

    def __init__(self, name: str, command: str):
        self.name = name
        self.command = command
        self.parameters: Dict[str, Any] = {}

    def _validate_parameters(self, user_parameters: Dict[str, Any]) -> None:
        missing_params = []
        for name in self.parameters:
            if name not in user_parameters and self.parameters[name].default is None:
                missing_params.append(name)
        if missing_params:
            raise ExecutionException(
                "No value given for missing parameters: %s"
                % ", ".join(["'%s'" % name for name in missing_params])
            )

    def compute_parameters(
        self, user_parameters: Optional[Dict[str, Any]]
    ) -> Tuple[Dict[str, Optional[str]], Dict[str, Optional[str]]]:
        """
        Given a dict mapping user-specified param names to values, computes parameters to
        substitute into the command for this entry point. Returns a tuple (params, extra_params)
        where `params` contains key-value pairs for parameters specified in the entry point
        definition, and `extra_params` contains key-value pairs for additional parameters passed
        by the user.
        """
        if user_parameters is None:
            user_parameters = {}
        # Validate params before attempting to resolve parameter values
        self._validate_parameters(user_parameters)
        final_params = {}
        extra_params = {}

        parameter_keys = list(self.parameters.keys())
        for key in parameter_keys:
            param_obj = self.parameters[key]
            key_position = parameter_keys.index(key)
            value = (
                user_parameters[key]
                if key in user_parameters
                else self.parameters[key].default
            )
            final_params[key] = param_obj.compute_value(value, key_position)
        for key in user_parameters:
            if key not in final_params:
                extra_params[key] = user_parameters[key]
        return (
            self._sanitize_param_dict(final_params),
            self._sanitize_param_dict(extra_params),
        )

    def compute_command(self, user_parameters: Optional[Dict[str, Any]]) -> str:
        params, extra_params = self.compute_parameters(user_parameters)
        command_with_params = self.command.format(**params)
        command_arr = [command_with_params]
        command_arr.extend(
            [
                "--%s %s" % (key, value) if value is not None else "--%s" % (key)
                for key, value in extra_params.items()
            ]
        )
        return " ".join(command_arr)

    @staticmethod
    def _sanitize_param_dict(param_dict: Dict[str, Any]) -> Dict[str, Optional[str]]:
        return {
            (str(key)): (quote(str(value)) if value is not None else None)
            for key, value in param_dict.items()
        }


def get_entry_point_command(
    entry_point: "EntryPoint", parameters: Dict[str, Any]
) -> List[str]:
    """
    Returns the shell command to execute in order to run the specified entry point.
    :param project: Project containing the target entry point
    :param entry_point: Entry point to run
    :param parameters: Parameters (dictionary) for the entry point command
    """
    commands = []
    commands.append(entry_point.compute_command(parameters))
    return commands


def create_project_from_spec(run_spec: Dict[str, Any], api: Api) -> Project:
    uri = run_spec["uri"]
    project, entity, run_id = utils.set_project_entity_defaults(
        uri, run_spec.get("project"), run_spec.get("entity"), api
    )
    if run_spec.get("name"):
        name = run_spec["name"]
    else:
        name = "{}_{}_launch".format(project, run_id)  # default naming scheme

    return Project(
        uri,
        entity,
        project,
        name,
        run_spec.get("docker", {}),
        run_spec.get("git", {}),
        run_spec.get("overrides", {}),
    )


def fetch_and_validate_project(project: Project, api: Api) -> Project:
    project._fetch_project_local(api=api)
    project._copy_config_local()
    first_entry_point = list(project._entry_points.keys())[0]
    project.get_entry_point(first_entry_point)._validate_parameters(
        project.override_args
    )
    return project
