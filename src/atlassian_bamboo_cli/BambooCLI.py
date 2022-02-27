# !/usr/bin/env python
# title           : BambooCLI.py
# description     : This module can work with Atlassian Client-side command line "acli" to be sent from
#                   the current shell. The pre-requisites for running these commands are to setup acli.properties file
#                   to be used for setting user authentication and bamboo instance
#                   root example : "http://localhost:8085/"
# author          : monkey-coder
# creation date   : 01/02/2022
# last updated    : 01/02/2022
# version         : 1.0
# usage           : import the BambooActions class, instantiate the class to send a command use the send_command().
# notes           : these are basic Bamboo CLI wrapped in python functions.
# python_version  : 3.9.2
# ==============================================================================

import subprocess
import os


class BambooTasks(object):
    """"""
    def __init__(self):
        self.task_type = ''
        self.task_dict = {'SCRIPT': {'interpreter': '', 'script_location': '',
                                     'script_body': '', 'argument': '', 'environment_variables': '',
                                     'working_sub_directory': ''},
                          'CHECKOUT': {'repository': '', 'force_clean_build': ''},
                          'INJECT_VARIABLES': {'path_to_properties': '', 'namespace': '', 'scope_of_variables': ''},
                          'CLEAN': {},
                          'ANT': {},
                          'ARTIFACT_DOWNLOAD': {},
                          'CLI_BAMBOO': {},
                          'CLI_BITBUCKET': {},
                          'CLI_CONFLUENCE': {},
                          'CLI_CRUCIBLE': {},
                          'CLI_FISHEYE': {},
                          'CLI_JIRA': {},
                          'CLI_SERVICE_DESK': {},
                          'CLI_SLACK': {},
                          'CLI_UPM': {},
                          'GANT': {},
                          'GINT': {},
                          'GRADLE': {},
                          'GRADLEW': {},
                          'GRADLEWRAPPER': {},
                          'GROOVY': {},
                          'JUNIT_PARSER': {},
                          'MAVEN2': {},
                          'MAVEN3': {},
                          'MAVEN_POM_EXTRACTOR': {},
                          'SCP': {},
                          'SQL': {},
                          'SSH': {},
                          'VARIABLE_REPLACE': {},
                          'com.atlassian.bamboo.plugin.dotnet:msbuild': {}
                          }

    def get_task_key(self, task_key):
        """Verifies the task key and returns the task parameters"""
        for key, value in self.task_dict.iteritems():
            if str(key).upper() == str(task_key).upper():
                return key
        raise KeyError(str.format('{0} task key not found', task_key))

    def get_task_value(self, task_key):
        for key, value in self.task_dict.iteritems():
            if str(key).upper() == str(task_key).upper():
                return value
        raise KeyError(str.format('{0} task key not found', task_key))


class BambooException(Exception):
    """"""
    pass


class BambooActions(object):
    """
    These are the keywords that tell the CLI what action to take. The actions listed correspond to nearly
    everything you can do via the screens on the app by pointing, clicking, and typing text into fields.
    You see a pattern to the beginning or prefix that is an action verb such as: add, copy, export, get,
    modify, move, remove, run, store, update, and more depending on the app. The ending or suffix to
    the action name is the noun or object of the verb such as attachment, comment, label, permission,
    user, and more depending on the app. For example, the action addComment adds a comment to an item
    in the app. Not all actions are available for all apps because not all apps have the same features.
    Arguments:
        bamboo_project_name: Name of the bamboo project where you want to create your plans.
        acli_directory_path: Path to the ACLI directory (after unzipping)
        acli_bamboo_server_name: Name of the bamboo server mentioned in the 'ACLI.properties'
            file within the ACLI directory
    Examples:
    """
    def __init__(self, bamboo_project_name, acli_directory_path, acli_bamboo_server_name):
        """"""
        self.project = bamboo_project_name
        self.acli_directory_path = acli_directory_path
        self.bamboo_server_name = acli_bamboo_server_name
        self.bamboo_tasks = BambooTasks()

    @staticmethod
    def add_optional_arguments(command, **kwargs):
        """"""
        command_list = list()
        command_list.append(command)
        for key, value in kwargs.items():
            if (value is None) or (value is False):
                continue
            elif value is True:
                command_list.append(str.format('--{0}', key))
            elif key.upper() == 'CONTINUES':
                command_list.append(str.format('--continue'))
            elif key.upper() == 'FAVORITE':
                command_list.append(str.format('--favorite'))
            elif key.upper() == 'EXCLUDE_DISABLED':
                command_list.append(str.format('--exclude_disabled'))
            elif key.upper() == 'EXCLUDE_ENABLED':
                command_list.append(str.format('--exclude_enabled'))
            else:
                command_list.append(str.format('--{0} "{1}"', key, value))

        return ' '.join(command_list)

    @staticmethod
    def create_run_input_from_list(input_list):
        """"""
        input_string = ""
        return input_string

    def create_plan(self, plan_name=None, project_name=None, name=None, description=None, repository=None,
                    disable=None, replace=False, continues=False, options=None):
        """
        Create a new plan. Provide a 2-part plan key where the first part is the project key. If the project key
        does not exist, it will be created with the provided project name.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            name: name of the plan. Type string. (Optional)
            project_name: name of the project. (Optional)
            description: a description of the plan what it needs to do. (Optional)
            repository: Bitbucket/GIT repository name. (Optional)
            disable: action to disable the plan. (Optional)
            replace: replace an existing plan, which, by default, follows a move, delete, create scenario. (Optional)
            continues: to ignore the request if the plan already exists. (Optional)
            options: Use '--options clear' to modify the replace scenario to only clearing most plan constructs
                    so they can be reconstructed later. Use '--options addDefaultJob' to automatically add
                    a default stage and job to the plan similar to creating a plan from the UI.
                    Use '--options removeTrigger' to automatically remove the default polling trigger added
                    when the repository parameter is specified. (Optional)
        Examples:
            create_plan(plan_name="ZCREATE4739509-AA", project_name="ZCREATE4739509 created project")
            create_plan(plan_name="ZCREATE4739509-BB", name="Simple plan BB", description="Simple plan BB description")
            create_plan(plan_name="ZCREATE4739509-CC", options="addDefaultJob")
            create_plan(plan_name="ZCREATE4739509-EMPTY", project_name="ZCREATE4739509 created project", replace=True,
                                                                                                        options="clear")
            create_plan(plan_name="ZCREATE4739509-EMPTY", continues=True)
        """

        if project_name is None:
            project_name = self.project
        command = str.format('--action createPlan --plan "{0}" --replace', plan_name)
        return self.add_optional_arguments(command, projectName=project_name, name=name, description=description,
                                           repository=repository, disable=disable, replace=replace, continues=continues,
                                           options=options)

    def add_stage(self, plan_name=None, stage=None, name=None, description=None, manual=None,
                  final=False, continues=None):
        """
        Add a stage to a plan.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            stage: name/id of the stage. Type string. (Mandatory)
            name: name of the stage. Type string. (Optional)
            description: a description of the stage. Type string. (Optional)
            manual: name/id of the plan. Type string. (Optional)
            final: to set the stage as final or not. Type boolean. (Optional)
            continues: to ignore the request if the stage already exists. Type boolean. (Optional)
        Examples:
            add_stage(plan_name="ZCREATE4739509-AA", name="My stage 2", description="My stage description")
            add_stage(plan_name="ZCREATE4739509-AA", stage="My stage 1", description="My stage description")
            add_stage(plan_name="ZCREATE4739509-AA", stage="Stage 1")
        """
        command = str.format('--action addStage --plan @plan@ --stage "{1}"', plan_name, stage)
        return self.add_optional_arguments(command, name=name, description=description, manual=manual, final=final,
                                           continues=continues)

    def add_job(self, plan_name=None, stage=None, job=None, name=None, description=None,
                type_name=None, docker=None, disable=False):
        """
        Add a job to a stage.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            stage: name/id of the stage. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            name: name of the job. Type string. (Optional)
            description: a description of the stage. Type string. (Optional)
            type_name: name/id of the plan. Type string. (Optional)
            docker: to set the stage as final or not. Type boolean. (Optional)
            disable: to ignore the request if the stage already exists. Type boolean. (Optional)
        Examples:
            add_job(plan_name="ZCREATE4739509-AA", stage="My stage 1", job="my job another",
                                                            description="My job 1 description")
            add_job(plan_name="ZCREATE4739509-AA", stage="My stage 1", job="REMOVE")
            add_job(plan_name="ZCREATE4739509-AA", stage="My stage 1", job="myjob", name="myjob 1")
            add_job(plan_name="ZCREATE4739509-BB", stage="Stage 1", job="JOB")
            add_job(plan_name="ZCREATE4739509-CC", stage="Default Stage", job="JOBDocker", type="Docker",
                                                                                        docker="myDocker")
        """
        command = str.format('--action addJob --plan @plan@ --stage @stage@ --job "{2}"', plan_name, stage, job)
        return self.add_optional_arguments(command, name=name, description=description, type_name=type_name,
                                           docker=docker, disable=disable)

    def add_task(self, plan_name=None, job=None, task_key=None, description=None, disable=False,
                 final=False, field=None, fields=None, field1=None, value1=None, field2=None, value2=None):
        """
        Add a task to a plan job. A valid task key or alias is required.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            task_key: is a unique key for performing specific activities in the given task.Please check the
             get_task_key in this class to find the list of task keys. (Mandatory)
            description: a description of the stage. Type string. (Optional)
            disable: to set a task as disabled. (Optional)
            final: to set a task as final. (Optional)
            field: accepts key=value pair. The field changes depending on the task key. (Optional)
            fields: accepts list of key:value pairs separated by comma. The field changes depending
                        on the task key. (Optional)
            field1: accepts a key name for the field like "scriptLocation". (Optional)
            value1: accepts a value for the field1 like "INLINE". (Optional)
            field2: accepts a key name for the field like "scriptBody". (Optional)
            value2: accepts a value for the field1 like "echo 'exitCode:\${bamboo.exitCode}';
                                                                exit \${bamboo.exitCode} ". (Optional)
        Examples:
            add_task(plan_name="ZBAMBOOCLI4825195-checkout1", job="JOB1", task_key="
                    com.atlassian.bamboo.plugins.scripttask:task.builder.script", description="task description",
                    fields="argument:aaaaa,environmentVariables:eeeee=vvvvv", field1="scriptLocation", value1="INLINE",
                    field2="scriptBody", value2="echo 'exitCode: \${bamboo.exitCode}'; exit \${bamboo.exitCode} ")
            add_task(plan_name="ZCLI-TASKS", job="JOB2", task_key="ARTIFACT_DOWNLOAD", field="sourcePlanKey=ZCLI-TASKS")
            add_task(plan_name="ZCLI-TASKS", job="JOB2", task_key="MAVEN_POM_EXTRACTOR")
            add_task(plan_name="ZEXPORT4891077-Export", job="JOB1", task_key="ARTIFACT_DOWNLOAD", field="
                    sourcePlanKey=ZEXPORT4891077-Export", field="artifactId_1=out.txt")
        """
        task_key = self.bamboo_tasks.get_task_key(task_key)
        command = str.format('--action addTask --plan @plan@ --job @job@ --taskKey "{2}"', plan_name, job, task_key)
        return self.add_optional_arguments(command,  description=description, disable=disable, final=final, field=field,
                                           fields=fields, field1=field1, value1=value1, field2=field2, value2=value2)

    def add_requirement(self, plan_name=None, job=None, requirement=None, req_type=None, value=None):
        """
        Add requirement to a plan job. Type defaults to EXISTS.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            requirements: this is like a pre-requisite and a mandatory requirement to run the job. It could
                         some software setup need on the bamboo agent or it can also be custom requirements. (Mandatory)
            req_type: type of the requirement like equal, not equal. (Optional)
            value: the given requirement should be "req_type" of value. (Optional)
        Examples:
            add_requirement(plan_name="ZCLI-REQUIREMENTS", job="JOB1", requirement="Ant")
            add_requirement(plan_name="ZCLI-REQUIREMENTS", job="JOB1", requirement="my-custom-requirement",
                            req_type="equal", value="mine")
            add_requirement(plan_name="ZCLI-REQUIREMENTS", job="JOB1", requirement="system.builder.gant.Gant")
        """
        command = str.format('--action addRequirement --plan @plan@ --job @job@ --requirement "{2}"', plan_name,
                             job, requirement)
        return self.add_optional_arguments(command, type=req_type, value=value)

    def add_repository(self, plan_name=None, name=None, repository_key=None, credentials=None, branch=None,
                       continues=None, replace=None, field=None, fields=None, field1=None, value1=None,
                       field2=None, value2=None):
        """
        Add a global or plan repository. If both a name and repository are provided, the name will be used for the
        Bamboo name and repository will be used for the Bitbucket reposiotry. For a plan repository,
        you can reference a linked (global) repository. Otherwise a valid repository key or alias is required.
        Valid aliases are: BITBUCKET, BITBUCKET_CLOUD, BITBUCKET_SERVER, STASH, BCVS, GIT, GITHUB, MERCURIAL,
        PERFORCE, SUBVERSION. If the credentials parameter is provided the appropriate fields will be added
        automatically for GIT, Mercurial, and Bitbucket Cloud repositories.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            name: name/id of the repository to add to the plan. (Mandatory)
            repository_key: repositories can be of different types. GIT, SVN. (Optional)
            credentials: username and password of the user. (Optional)
            branch: branch name from the repo. (Optional)
            replace: a specific revision can be built if the revision parameter is specified. (Optional)
            continues: this parameter is used to ignore a failed result. (Optional)
            field: accepts key=value pair. (Optional)
            fields: accepts list of key:value pairs separated by comma. (Optional)
            field1: accepts a key name for the field like "started". (Optional)
            value1: accepts a value for the field1 like "2020-03-30T08:25:39.514-0500". (Optional)
            field2: accepts a key name for the field like "state". (Optional)
            value2: accepts a value for the field1 like "SUCCESSFUL". (Optional)
        Examples:
            add_repository(plan_name="ZCLI-REQUIREMENTS", name="yieldstar")
            add_repository(plan_name="ZCLI-REQUIREMENTS", repository_key="GIT", name="groovy",
                            credentials="bitbucket-cloud-read-only",
                            fields="repository.git.repositoryUrl:
                            'https://bitbucket.org/bobswift/groovy',repository.git.branch:master,
                            repository.git.commandTimeout:2,selectedWebRepositoryViewer:
                            'bamboo.webrepositoryviewer.provided:noRepositoryViewer")
        """
        command = str.format('--action addRepository --plan @plan@ --name "{1}"', plan_name, name)
        return self.add_optional_arguments(command, branch=branch, repositoryKey=repository_key,
                                           credentials=credentials, replace=replace, continues=continues,
                                           field=field, fields=fields, field1=field1, value1=value1, field2=field2,
                                           value2=value2)

    def add_branch(self, plan_name=None, branch=None, name=None, description=None, continues=None, enable=True):
        """
        Add a branch to a plan. The plan branch will be disabled by default. For add, the branch parameter refers
        to the repository branch. An optional name for the plan branch can be specified, otherwise the
        repository branch name will be used.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            branch: name of the branch in git/bitbucket. (Mandatory)
            name: user defined name for the branch. (Optional)
            description: a description of the branch. Type string. (Optional)
            continues: this parameter is used to ignore a failed result. (Optional)
            enable: by default it is disabled. (Optional)
        Examples:
            add_branch(plan_name="ZCLI-REQUIREMENTS", branch="bugfix/YS-0101010-plan_branch")
            add_branch(plan_name="ZCLI-REQUIREMENTS", branch="bugfix/YS-0101010-plan_branch, name='mybranch'")
        """
        command = str.format('--action addBranch --plan @plan@ --branch "{1}"', plan_name, branch)
        return self.add_optional_arguments(command, name=name, description=description,
                                           continues=continues, enable=enable)

    def queue_build(self, plan_name=None, build=None, branch=None, revision=None, number=None, wait=False, stage=None,
                    continues=False, timeout=None, date_format=None, field=None, fields=None, field1=None, value1=None,
                    field2=None, value2=None):
        """
        Queue a build to run. If a build number is provided (number parameter or 3 part build key), an existing
        failed or incomplete build can be restarted. If wait is specified, the action will not complete until the
        queued build completes or the timeout period elapses. The action will fail if the build fails unless continue
        parameter is used to ignore a failed result. A specific revision can be built if the revision parameter is
        specified. Plan variables can be set using the field and value parameters. Plans with manual stages can be
        automatically continued to a specific stage or @ALL using the stage parameter provided wait is also used.
        Conditional queueing is supported - see the documentation for details.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory) OR
            build: name/id of the build. Type string. (Mandatory)
            branch: a git branch name. (Optional)
            revision: a specific revision can be built if the revision parameter is specified. (Optional)
            number: a build number. (Optional)
            wait: If wait is specified, the action will not complete until the queued build completes or the
                  timeout period elapses. (Optional)
            stage: a specific stage or or @ALL can be set using this parameter. (Optional)
            continues: this parameter is used to ignore a failed result. (Optional)
            timeout: to specific the time out for a build. (Optional)
            date_format: to specify a dat format like "yyyy-MM-dd HH:mm:ss". (Optional)
            field: accepts key=value pair. (Optional)
            fields: accepts list of key:value pairs separated by comma. (Optional)
            field1: accepts a key name for the field like "started". (Optional)
            value1: accepts a value for the field1 like "2020-03-30T08:25:39.514-0500". (Optional)
            field2: accepts a key name for the field like "state". (Optional)
            value2: accepts a value for the field1 like "SUCCESSFUL". (Optional)
        Examples:
            queue_build(plan_name="ZLONGRUNNING-AA")
            queue_build(build="XXX-FAIL", wait=True)
            queue_build(plan_name="ZLONGRUNNING-AA", wait=True, stage="@all")
            queue_build(build="ZBAMBOOCLI4825195-checkout1", wait=True, timeout=90, fields="exitCode: 0")
            queue_build(plan_name="ZCREATE4739509-BB", field1="started", value1="2020-03-30T08:25:39.514-0500",
                        field2="state", value2="SUCCESSFUL")
            queue_build(plan_name="ZLONGRUNNING-AA", branch="2.5.0", wait=True)
        """
        if build is not None:
            command = str.format('--action queueBuild --build "{0}"', build)
        else:
            command = str.format('--action queueBuild --plan "{0}"', plan_name)
        return self.add_optional_arguments(command, branch=branch, revision=revision, number=number, wait=wait,
                                           stage=stage, continues=continues, timeout=timeout, dateFormat=date_format,
                                           field=field, fields=fields, field1=field1, value1=value1, field2=field2,
                                           value2=value2)

    def get_build(self, build=None, number=None, file_name=None, encoding=None, date_format=None):
        """
        Get build result.
        Arguments:
            build: name/id of the build. Type string. (Mandatory)
            number: build number like ZCREATE4739509-BB-3. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
            date_format: to specify a dat format like "yyyy-MM-dd HH:mm:ss". (Optional)
        Examples:
            get_build(build="XXX-DEF", dateFormat="yyyy-MM-dd HH:mm:ss")
            get_build(build="XXX-DEF-232")
            get_build(build="ZCREATE4739509-BB-3", dateFormat="yyyy-MM-dd HH:mm:ss.SSS")
        """
        command = str.format('--action getBuild --build "{0}"', build)
        return self.add_optional_arguments(command, number=number, file=file_name, encoding=encoding,
                                           dateFormat=date_format)

    def get_build_log(self, build=None, job=None, number=None, limit=None, regex=None,
                      find_replace=None, find_replace_regex=None, file_name=None, encoding=None):
        """
        Get log entries for a build result with regex filtering of the lines to be included.
        Use the limit parameter to only show the last number of selected lines.
        Find and replace parameters can be used to modify the selected line output.
        Log lines have 3 tab separated columns with type, timestamp, and detail elements.
        Arguments:
            build: name/id of the build. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            number: build number like ZCREATE4739509-BB-3. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
            regex: a regular expression to select the jobs. (Optional)
            limit: to limit the number of build results retrieved. By default set to 25. (Optional)
            find_replace: Successively find and replace matching text with the find and replace values specified
                          using find:replace syntax. The first colon (:) delineates the find value from the replace
                          value. Single quote values containing a color and then escape embedded quotes. Deprecated
                          use is a comma separated list of the same. Recommend using multiple parameters instead.
                          The deprecated use case is only valid when the multiple parameter feature is not
                          being used. (Optional)
            find_replace_regex: Successively find and replace matching text with the find and replace values
                                specified using find:replace syntax. The first colon (:) delineates the find value
                                from the replace value. Single quote values containing a color and then escape
                                embedded quotes. The find value must be a valid regular regular expression and
                                the replace value can contain replacement variables for capture groups like $1,
                                $2, and so on. For some command shells, the $ may need to be escaped. Deprecated
                                use is a comma separated list of the same. Recommend using multiple parameters
                                instead. The deprecated use case is only valid when the multiple parameter
                                feature is not being used. (Optional)
        Examples:
            get_build(build="XXX-DEF", dateFormat="yyyy-MM-dd HH:mm:ss")
            get_build(build="XXX-DEF-232")
            get_build(build="ZCREATE4739509-BB-3", dateFormat="yyyy-MM-dd HH:mm:ss.SSS")
        """
        command = str.format('--action getBuildLog --build "{0}"', build)
        return self.add_optional_arguments(command, job=job, number=number, file=file_name, encoding=encoding,
                                           limit=limit, regex=regex, findReplace=find_replace,
                                           findReplaceRegex=find_replace_regex)

    def get_branch_list(self, plan_name=None, limit=None, regex=None, columns=None, file_name=None,
                        append=None, encoding=None):
        """
        Get a list of jobs for a plan with regex filtering on job key or name. Subset by stage if desired.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            regex: a regular expression to select the jobs. (Optional)
            limit: to limit the number of build results retrieved. By default set to 25. (Optional)
            columns: columns to select for the results like plan,duration description,labels,issues. (Optional)
            append: append the columns to be included. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
        Examples:
            --action getBranchList --plan "ZCREATE4739509-CC"
            --action getBranchList --plan "ZCREATE4739509SCRIPT-PLAN" --regex "TEST2.*"
                --outputType "table"
        """
        command = str.format('--action getBranchList --plan "{0}"', plan_name)
        return self.add_optional_arguments(command, limit=limit, regex=regex, columns=columns,
                                           file=file_name, append=append, encoding=encoding)

    def get_build_list(self, plan_name=None, labels=None, issues=None, limit=None, columns=None, file_name=None,
                       append=None, encoding=None, date_format=None, field=None, fields=None, field1=None,
                       value1=None, field2=None, value2=None, output_format=None):
        """
        Get a list of build results. Build results can be filtered by labels, issues, and using field parameters.
        Supported fields are state, notState, started, endedBefore. For example, include only successful results
        by using: --field state=SUCCESSFUL, or include only builds started after a specific date use: --field
        started=2016-04-30 --dateFormat yyyy-MM-dd. Default limit is 25.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            labels: used to filter the list of build results. (Optional)
            issues: used to filter the list of build results. (Optional)
            limit: to limit the number of build results retrieved. By default set to 25. (Optional)
            columns: columns to select for the results like plan,duration description,labels,issues. (Optional)
            append: append the columns to be included. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
            date_format: to specify a dat format like "yyyy-MM-dd HH:mm:ss". (Optional)
            field: accepts key=value pair. (Optional)
            fields: accepts list of key:value pairs separated by comma. (Optional)
            field1: accepts a key name for the field like "started". (Optional)
            value1: accepts a value for the field1 like "2020-03-30T08:25:39.514-0500". (Optional)
            field2: accepts a key name for the field like "state". (Optional)
            value2: accepts a value for the field1 like "SUCCESSFUL". (Optional)
            output_format: format of the resultant list. (Optional)
        Examples:
            get_build_list(plan_name="ZLONGRUNNING-AA")
            get_build_list(plan_name="ZCLI-BUILDLIST", limit=1, output_format=999, issues="NOTFOUND-123")
            get_build_list(plan_name="ZCLI-BUILDLIST", limit=1, output_format=999, labels="not_found,testlabel1")
            get_build_list(plan_name="ZLONGRUNNING-AA", filed1="STARTED", value1="2020-03-30T08:28:31.180-0500",
                           outputFormat=2, date_format="yyyy-MM-dd'T'HH:mm:ss.SSSZ")
            get_build_list(plan_name="ZLONGRUNNING-AA", dateFormat="yyyy-MM-dd HH:mm:ss.SSS", output_format=999,
                           columns="build,number,state,started,completed")
        """
        command = str.format('--action getBuildList --plan "{0}"', plan_name)
        return self.add_optional_arguments(command, labels=labels, issues=issues, limit=limit, columns=columns,
                                           file=file_name, append=append, encoding=encoding, field=field, fields=fields,
                                           field1=field1, value1=value1, field2=field2, value2=value2,
                                           dateFormat=date_format, outputFormat=output_format)

    def get_job(self, plan_name=None, job=None):
        """
        Get job information.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
        Examples:
            get_job(plan_name="ZCREATE4739509-CC", job="JOB1")
            get_job(plan_name="ZCREATE4739509-CC", job="JOBDocker")
        """
        command = str.format('--action getJob --plan "{0}" --job "{1}"', plan_name, job)
        return self.add_optional_arguments(command)

    def get_job_list(self, plan_name=None, stage=None, limit=None, regex=None, columns=None, file_name=None,
                     append=None, encoding=None):
        """
        Get a list of jobs for a plan with regex filtering on job key or name. Subset by stage if desired.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            stage: a specific stage or or @ALL can be set using this parameter. (Optional)
            regex: a regular expression to select the jobs. (Optional)
            limit: to limit the number of build results retrieved. By default set to 25. (Optional)
            columns: columns to select for the results like plan,duration description,labels,issues. (Optional)
            append: append the columns to be included. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
        Examples:
            --action getJobList --plan "ZCREATE4739509-AA" --job "@all" --stage "My stage 1" --columns "enabled,type"
            --action getJobList --plan "ZCREATE4739509-CC"
            --action getJobList --plan "ZCREATE4739509SCRIPT-PLAN"
            --action getJobList --plan "ZCREATE4739509SCRIPT-PLAN" --regex "TEST2.*"
            --action getJobList --plan "ZCREATE4739509SCRIPT-PLAN" --regex "TEST2.*" --columns "stage,job"
                --outputType "table"
        """
        command = str.format('--action getJobList --plan "{0}"', plan_name)
        return self.add_optional_arguments(command, stage=stage, limit=limit, regex=regex, columns=columns,
                                           file=file_name, append=append, encoding=encoding)

    def get_plan(self, plan_name=None):
        """
        Get plan information.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
        Examples:
            --action getPlan --plan "ZBAMBOOCLI4825195-checkout1"
        """
        command = str.format('--action getPlan --plan "{0}"', plan_name)
        return self.add_optional_arguments(command)

    def get_plan_list(self, project_name=None, favorite=False, exclude_disabled=False, exclude_enabled=False,
                      labels=None, options=None, limit=None, regex=None, output_format=None, date_format=None,
                      columns=None, file_name=None, append=None, encoding=None, field=None,
                      fields=None, field1=None, value1=None, field2=None, value2=None):
        """
        Get a list of plans for a project with regex filtering on plan key or name. Additionally, use labels
        parameter to filter by labels. Use @all for project to get a list of plans across all projects. To also
        include branch plans in the list, use --options "includeBranchPlans". Advanced filtering based on state
        and date of the latest build for the plan is also available. See getBuildList for more information.
        Advanced filtering based on using a repository is also possible using --options "usingRepository=xxx".
        Arguments:
            project_name: name/id of the project. Type string. (Mandatory)
            favorite: to get the projects which are set as favorites with "@all". (Optional)
            exclude_disabled: to exclude the disabled projects in the bamboo master. (Optional)
            exclude_enabled: to exclude the enabled projects. (Optional)
            options: are used to set repositories like "usingRepository=zrepositories git". (Optional)
            regex: a regular expression to select the jobs. (Optional)
            labels: used to filter the list of build results. (Optional)
            limit: to limit the number of build results retrieved. By default set to 25. (Optional)
            columns: columns to select for the results like plan,duration description,labels,issues. (Optional)
            append: append the columns to be included. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
            date_format: to specify a dat format like "yyyy-MM-dd HH:mm:ss". (Optional)
            field: accepts key=value pair. (Optional)
            fields: accepts list of key:value pairs separated by comma. (Optional)
            field1: accepts a key name for the field like "started". (Optional)
            value1: accepts a value for the field1 like "2020-03-30T08:25:39.514-0500". (Optional)
            field2: accepts a key name for the field like "state". (Optional)
            value2: accepts a value for the field1 like "SUCCESSFUL". (Optional)
            output_format: format of the resultant list. (Optional)
        Examples:
            --action getPlanList --project "@all" --excludeDisabled --outputFormat 999 --dateFormat
            "yyyy-MM-dd HH:mm:ss"
            --action getPlanList --project "@all" --favorite
            --action getPlanList --project "@all" --file "output/create/getPlanList.txt"
            --action getPlanList --project "XXX" --options "usingRepository=zrepositories git"
            --action getPlanList --project "ZMOVE4738525"
        """
        if project_name is None:
            project_name = self.project
        command = str.format('--action getPlanList --project "{0}"', project_name)
        return self.add_optional_arguments(command, favorite=favorite, excludeDisabled=exclude_disabled,
                                           excludeEnabled=exclude_enabled, labels=labels, options=options,
                                           limit=limit, regex=regex, outputFormat=output_format,
                                           dateFormat=date_format, columns=columns, file=file_name,
                                           append=append, encoding=encoding, field=field, fields=fields,
                                           field1=field1, value1=value1, field2=field2, value2=value2)

    def get_project(self, project_name=None):
        """
        Get project.
        Arguments:
            project_name: name/id of the project. Type string. (Mandatory)
        Examples:
            get_project(project="ZPROJECTS4747077")
        """
        if project_name is None:
            project_name = self.project
        command = str.format('--action getProject --project "{0}"', project_name)
        return self.add_optional_arguments(command)

    def get_stage(self, plan_name, stage):
        """
        Get plan stage information.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            stage: name/id of the stage. Type string. (Mandatory)
        Examples:
            get_stage(plan_name="ZCREATE4739509SCRIPT-PLAN", stage="B updated")
            get_stage(plan_name="ZCREATE4739509SCRIPT-PLAN", stage="B")

        """
        command = str.format('--action getStage --plan "{0}" --stage "{1}"', plan_name, stage)
        return self.add_optional_arguments(command)

    def get_stage_list(self, plan_name, regex=None, columns=None, file_name=None, append=None, encoding=None):
        """
        Get a list of stages for a plan with regex filtering on stage name.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            regex: a regular expression to select the jobs. (Optional)
            columns: columns to select for the results like plan,duration description,labels,issues. (Optional)
            append: append the columns to be included. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
        Examples:
            get_stage_list(plan_name="ZCREATE4739509SCRIPT-PLAN")
            get_stage_list(plan_name="ZCREATE4739509SCRIPT-PLAN", regex="A.*")
        """
        command = str.format('--action getStageList --plan "{0}"', plan_name)
        return self.add_optional_arguments(command, regex=regex, columns=columns, file=file_name,
                                           append=append, encoding=encoding)

    def get_task(self, plan_name, job, task):
        """
        Get detail information on a task from a plan job. Use --task @all to give detail
        information on all tasks for a job.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            task: task name/id of the task. Type string. (Mandatory)
        Examples:
            get_task(plan_name="ZCLI-TASKS", job="JOB", task="@all")
            get_task(plan_name="ZCLI-TASKS", job="JOB", task=1)
        """
        command = str.format('--action addTask --plan "{0}" --job "{1}" --task "{2}"', plan_name, job, task)
        return self.add_optional_arguments(command)

    def run(self, file_path=None, inputs=None, common=None, continues=None, simulate=False, field=None,
            encoding=None, clear_file_before_append=False, find_replace=None, find_replace_regex=None,
            date_format=None):
        """
        Run actions from a file, list of input parameters, or standard input (default).
        Arguments:
            file_path: complete valid text file path for running the commands in that file. (Optional)
            inputs: a list of commands which will be used as input for the run command. (Optional)
            common: run this command command for all the commands from the file or the input list. (Optional)
            continues: this parameter is used to ignore a failed result. (Optional)
            simulate: simulate running actions. Log the action that would be taken. (Optional)
            field: accepts key=value pair. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
            clear_file_before_append: for run action, this option will automatically clear an existing
                                     file on the first append requested. (Optional)
            find_replace: Successively find and replace matching text with the find and replace values specified
                          using find:replace syntax. The first colon (:) delineates the find value from the replace
                          value. Single quote values containing a color and then escape embedded quotes. Deprecated
                          use is a comma separated list of the same. Recommend using multiple parameters instead.
                          The deprecated use case is only valid when the multiple parameter feature is not
                          being used. (Optional)
            find_replace_regex: Successively find and replace matching text with the find and replace values
                                specified using find:replace syntax. The first colon (:) delineates the find value
                                from the replace value. Single quote values containing a color and then escape
                                embedded quotes. The find value must be a valid regular regular expression and
                                the replace value can contain replacement variables for capture groups like $1,
                                $2, and so on. For some command shells, the $ may need to be escaped. Deprecated
                                use is a comma separated list of the same. Recommend using multiple parameters
                                instead. The deprecated use case is only valid when the multiple parameter
                                feature is not being used. (Optional)
            date_format: to specify a dat format like "yyyy-MM-dd HH:mm:ss". (Optional)
        Examples:
            --action run
            run()
            run(file_path="./src/itest/bamboo/resources/create-plan-standard-tasks.txt",
                find_replace="%project%:ZCREATE4739509,%plan%:STANDARDTASKSFROMLIST")
            run(file_path="./src/itest/bamboo/resources/create-plan.txt",
                find_replace="%PLAN%:ZDEVELOPER4816315SCRIPT-PLAN,%PLAN_NAME%:Plan created by script by developer,
                              %PLAN_DESCRIPTION%:Plan description,%PROJECT_NAME%:Project created by script
                              4816315,%STAGE_DESCRIPTION%:First stage,%AGENT%:Z Added 1")
            run(input=["-a createPlan --plan ZCLI-TASKS --replace",
                       "-a addVariables --plan @plan@ --field exitCode --value 0",
                       "-a addStage --plan @plan@ --stage FIRST",
                       "-a addJob --plan @plan@ --stage @stage@ --job JOB",
                       " -a runFromList --list ,BBB,CCC,DDD,EEE --list2 ,--disable --common \\"-a addTask --plan
                       @plan@ --job @job@ --taskKey SCRIPT --description \\"@entry@\\" @entry2@ --field
                       scriptLocation=INLINE --field scriptBody=xxx\\" " --input "-a addTask --plan @plan@
                       --job @job@ --taskKey SCRIPT --description FFF --field scriptLocation=INLINE --field
                       scriptBody=xxx --final -v" --input "-a addJob --plan @plan@ --stage @stage@ --job JOB2"])
            run(input=["-a addVariables --field \\"aaa=AAA\\" --replace",
                       "-a getVariableList --reference bamboo. -f \\"\\"",
                       "-a getClientInfo --comment @bamboo.aaa@"])
        """
        if inputs is not None:
            inputs = self.create_run_input_from_list(inputs)
        command = str.format('--action run')
        return self.add_optional_arguments(command, file=file_path, input=inputs, common=common,
                                           continues=continues, simulate=simulate, field=field,
                                           encoding=encoding, clearFileBeforeAppend=clear_file_before_append,
                                           findReplace=find_replace, findReplaceRegex=find_replace_regex,
                                           dateFormat=date_format)

    def restart_build(self, plan_name=None, wait=False, stage=None, timeout=None, continues=None):
        """
        Disable a job from running. Use @all for job to disable all jobs in a stage.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            stage: name/id of the stage. Type string. (Optional)
            wait: If wait is specified, the action will not complete until the queued build completes or the
                  timeout period elapses. (Optional)
            timeout: to specific the time out for a build. (Optional)
            continues: this parameter is used to ignore a failed result. (Optional)
        Examples:
            restart_build(plan_name="ZLONGRUNNING-AA", stage="@ALL", wait=True)
            restart_build(plan_name="ZLONGRUNNING-AA", stage="THIRD", wait=True)
        """
        command = str.format('--action restartBuild --plan "{0}"', plan_name)
        return self.add_optional_arguments(command, wait=wait, stage=stage, timeout=timeout, continues=continues)

    def stop_build(self, plan_name, wait=False, timeout=None, continues=None):
        """
        Request to stop a queued or running build. Use continue to ignore errors finding a build to stop
        or failed results. The wait parameter will cause processing to wait for completion or timeout before returning.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            wait: If wait is specified, the action will not complete until the queued build completes or the
                  timeout period elapses. (Optional)
            timeout: to specific the time out for a build. (Optional)
            continues: this parameter is used to ignore a failed result. (Optional)
        Examples:
            stop_build(plan_name="ZLONGRUNNING-AA", wait=True)
        """
        command = str.format('--action stopBuild --plan "{0}"', plan_name)
        return self.add_optional_arguments(command, wait=wait, timeout=timeout, continues=continues)

    def disable_job(self, plan_name, job, stage=None):
        """
        Disable a job from running. Use @all for job to disable all jobs in a stage.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            stage: name/id of the stage. Type string. (Optional)
        Examples:
            disable_job(plan_name="ZCREATE4739509-AA", job="@all", stage="My stage 1")
            disable_job(plan_name="ZCREATE4739509-AA", job="myjob")
        """
        command = str.format('--action disableJob --plan "{0}" --job "{1}"', plan_name, job)
        return self.add_optional_arguments(command, stage=stage)

    def disable_plan(self, plan_name):
        """
        Disable a plan from running.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
        Examples:
            disable_plan(plan_name="ZBAMBOOCLI4825195-checkout1")
            disable_plan(plan_name="ZBAMBOOCLI4825195-notask")
        """
        command = str.format('--action disableJob --build "{0}"', plan_name)
        return self.add_optional_arguments(command)

    def enable_job(self, plan_name, job, stage=None):
        """
        Enable a job to run. Use @all for job to enable all jobs in a stage.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            stage: name/id of the stage. Type string. (Optional)
        Examples:
            enable_job(plan_name="ZCREATE4739509-AA", job="MYJOB")
            enable_job(plan_name="ZCREATE4739509-AA", job="myjob")
        """
        command = str.format('--action enableJob --plan "{0}" --job "{1}"', plan_name, job)
        return self.add_optional_arguments(command, stage=stage)

    def enable_plan(self, plan_name):
        """
        Enable a plan to run.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
        Examples:
            enable_plan(plan_name="ZBAMBOOCLI4825195-checkout1")
            enable_plan(plan_name="ZBAMBOOCLI4825195-notask")
        """
        command = str.format('--action enablePlan --build "{0}"', plan_name)
        return self.add_optional_arguments(command)

    def delete_plan(self, plan_name):
        """
        Delete a plan.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
        Examples:
            delete_plan(plan_name="ZBAMBOOCLI4825195-checkout1")
        """
        command = str.format('--action deletePlan --plan "{0}"', plan_name)
        return self.add_optional_arguments(command)

    def remove_job(self, plan_name, job, continues=None):
        """
        Remove a stage from a plan. Use --stage @all to remove all stages. Use continue to ignore not found errors.
        On Bamboo 6.8 and higher, stages are removed in the background. Use *wait* to wait for the background
        removal to occur before completing the action.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            continues: this parameter is used to ignore a failed result. (Optional)
        Examples:
            remove_job(plan_name="ZCREATE4739509-AA", job="REMOVE")
        """
        command = str.format('--action removeJob --plan "{0}" --job "{1}"', plan_name, job)
        return self.add_optional_arguments(command, continues=continues)

    def remove_stage(self, plan_name, stage, wait=False, timeout=None, continues=None):
        """
        Remove a stage from a plan. Use --stage @all to remove all stages. Use continue to ignore not found errors.
        On Bamboo 6.8 and higher, stages are removed in the background. Use *wait* to wait for the background
        removal to occur before completing the action.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            stage: name/id of the stage. Type string. (Mandatory)
            wait: If wait is specified, the action will not complete until the queued build completes or the
                  timeout period elapses. (Optional)
            continues: this parameter is used to ignore a failed result. (Optional)
            timeout: to specific the time out for a build. (Optional)
        Examples:
            remove_stage(plan_name="ZBAMBOOCLI4825195-checkout1", stage="SETUP")
        """
        command = str.format('--action removeStage --plan "{0}" --stage "{1}"', plan_name, stage)
        return self.add_optional_arguments(command, wait=wait, timeout=timeout, continues=continues)

    def remove_task(self, plan_name, job, task, task_id):
        """
        Remove a task from a plan job. Use --task @all to remove all tasks.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            task: task name of the task. Type string. (Mandatory) OR
            task_id: task id of the task. Type string. (Mandatory)
        Examples:
            remove_task(plan_name="ZCLI-TASKS", job="JOB1", task="@all")
            remove_task(plan_name="ZCLI-TASKS", job="JOB1", id=2)
        """
        if task is not None:
            command = str.format('--action removeTask --plan "{0}" --job "{1}" --task "{2}"', plan_name, job, task)
        else:
            command = str.format('--action removeTask --plan "{0}" --job "{1}" --id "{2}"', plan_name, job, id)
        return self.add_optional_arguments(command, job=job, task=task, id=task_id)

    def remove_requirement(self, plan_name, job, requirement, task_id):
        """
        Remove a plan requirement. Specify -1 for id to remove all requirements from a plan that are
        eligible to be removed.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            job: name/id of the job. Type string. (Mandatory)
            requirement: this is like a pre-requisite and a mandatory requirement to run the job. It could
                         some software setup need on the bamboo agent or it can also be custom requirements. (Mandatory)
            task_id: task id of the task. Type string. (Mandatory)
        Examples:
            remove_requirement(plan_name="ZCLI-TASKS", job="JOB1", requirement="SIML2", task_id=1)
        """
        command = str.format('--action removeRequirement --plan "{0}" --job "{1}" --requirement "{2}" --id {3}',
                             plan_name, job, requirement, id)
        return self.add_optional_arguments(command, job=job, requirement=requirement, id=task_id)

    def update_branching_options(self, plan_name=None, field=None, field1=None, value1=None,
                                 field2=None, value2=None, file_name=None, encoding=None):
        """
        Update branching options for a plan. Use the field or other field setting parameters to set options.
        Use getBranchingOptions to view the available fields that can be set.
        Arguments:
            plan_name: name/id of the plan. Type string. (Mandatory)
            field: accepts key=value pair. (Optional)
            field1: accepts a key name for the field like "started". (Optional)
            value1: accepts a value for the field1 like "2020-03-30T08:25:39.514-0500". (Optional)
            field2: accepts a key name for the field like "state". (Optional)
            value2: accepts a value for the field1 like "SUCCESSFUL". (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
        Examples:
            update_branching_options(plan_name="ZCLI-TASKS", field="planBranchCreationRegularExpression=<branch_name>")
            update_branching_options(plan_name="ZCLI-TASKS", field="planBranchCreationRegularExpression=YS-62330")
            update_branching_options(plan_name="ZCLI-TASKS", field="branchTriggering=manual")
        """
        command = str.format('--action updateBranchingOptions --plan "{0}"', plan_name)
        return self.add_optional_arguments(command, field=field, field1=field1, value1=value1, field2=field2,
                                           value2=value2, file_name=file_name, encoding=encoding)

    def enable_agent(self, agent_name):
        """
        Enable an agent.
        Arguments:
            agent_name: name of the bamboo agent to be enabled. (Mandatory)
        Examples:
            enable_agent(agent_name="YOUR_BAMBOO_AGENT_NAME")
        """
        command = str.format('--action enableAgent --agent "{0} ', agent_name)
        return self.add_optional_arguments(command)

    def disable_agent(self, agent_name):
        """
        Disable an agent.
        Arguments:
            agent_name: name of the bamboo agent to be disabled. (Mandatory)
        Examples:
            disable_agent(agent_name="YOUR_BAMBOO_AGENT_NAME")
        """
        command = str.format('--action disableAgent --agent "{0} ', agent_name)
        return self.add_optional_arguments(command)

    def get_agent_info(self, exclude_disabled=False, exclude_enabled=False, options=None, columns=None,
                       limit=None, regex=None, file_name=None, append=None, encoding=None, select=None):
        """
        Get a list of agents based on regex filtering of agent names.
        Arguments:
            exclude_disabled: to exclude the disabled projects in the bamboo master. (Optional)
            exclude_enabled: to exclude the enabled projects. (Optional)
            options: are used to set repositories like "usingRepository=zrepositories git". (Optional)
            regex: a regular expression to select the jobs. (Optional)
            limit: to limit the number of build results retrieved. By default set to 25. (Optional)
            append: append the columns to be included. (Optional)
            columns: columns to select for the results like plan,duration description,labels,issues. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
            select: Used for row selection by column value on list actions. The first colon (:) in
                the parameter value delineates the column name or number from a regex selection pattern.
                Each row's column value is used with the regex pattern to determined row inclusion in the
                final result. By default, row is included if the regex pattern is found in the
                column value. The options parameter can be set to one or more of the following to modify
                the default behavior: literal - to treat the regex string as a literal string, exact -
                to require an exact match of the value (not just a find!), negative - to reverse the
                condition so a match means exclude the row. Row selection takes place after all other
                action specific filtering conditions including the limit determination and so generally
                should not be used with the limit parameter. (Optional)
        Examples:
            get_agent_info()
            get_agent_info(regex="Z Added 3", columns="id")
            get_agent_info(excludeDisabled="True", outputFormat=2)
            get_agent_info(outputFormat=2)
            get_agent_info(outputFormat=999)
        """
        command = str.format('--action getAgentList ')
        return self.add_optional_arguments(command, excludeDisabled=exclude_disabled, columns=columns,
                                           excludeEnabled=exclude_enabled, options=options,
                                           limit=limit, regex=regex, file=file_name,
                                           append=append, encoding=encoding, select=select)

    def get_agent_assignment_list(self, agent_name, options=None, limit=None, capability_type=None, regex=None,
                                  file_name=None, append=None, encoding=None, select=None):
        """
        Get a list of assignments for agents with regex filtering on entity key or name.
        Specify an agent to filter by agent. Specify an assignment type to filter on type. Valid
        types are PROJECT, PLAN, JOB, DEPLOYMENT_PROJECT, ENVIRONMENT.
        Arguments:
            agent_name: name of the bamboo agent to be enabled. (Mandatory)
            options: are used to set repositories like "usingRepository=zrepositories git". (Optional)
            regex: a regular expression to select the jobs. (Optional)
            limit: to limit the number of build results retrieved. By default set to 25. (Optional)
            append: append the columns to be included. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
            capability_type: Capability type like Executable, Custom, or JDK.Also, requirement match type
                with values: exist (default), equal, match. Also, trigger type for addTrigger and
                job isolation type like agent or docker.. (Optional)
            select: Used for row selection by column value on list actions. The first colon (:) in
                the parameter value delineates the column name or number from a regex selection pattern.
                Each row's column value is used with the regex pattern to determined row inclusion in the
                final result. By default, row is included if the regex pattern is found in the
                column value. The options parameter can be set to one or more of the following to modify
                the default behavior: literal - to treat the regex string as a literal string, exact -
                to require an exact match of the value (not just a find!), negative - to reverse the
                condition so a match means exclude the row. Row selection takes place after all other
                action specific filtering conditions including the limit determination and so generally
                should not be used with the limit parameter. (Optional)
        Examples:
            get_agent_assignment_list(agent="zdeploy", regex=".*ZDEPLOY3505623.*")
        """
        command = '--action getAgentAssignmentList '
        return self.add_optional_arguments(command, agent=agent_name, type=capability_type, options=options,
                                           limit=limit, regex=regex, file=file_name,
                                           append=append, encoding=encoding, select=select)

    def get_agent_capability(self, agent_name, options=None, limit=None, regex=None, columns=None,
                             file_name=None, append=None, encoding=None, select=None):
        """
        Get a list of shared or agent specific capabilities with regex filtering on capability key or name (label).
        Use @all for agent to get shared and agent specific capabilities. Specify --options includeUnreferenced
        to include unreferenced server capabilities keys known to the system.
        Arguments:
            agent_name: name of the bamboo agent to be enabled. (Mandatory)
            options: are used to set repositories like "usingRepository=zrepositories git". (Optional)
            regex: a regular expression to select the jobs. (Optional)
            limit: to limit the number of build results retrieved. By default set to 25. (Optional)
            append: append the columns to be included. (Optional)
            columns: columns to select for the results like plan,duration description,labels,issues. (Optional)
            file_name: file path which contains the build data. (Optional)
            encoding: file encoding like UTF-8, UTF-16BE, UTF-32BE. (Optional)
            select: Used for row selection by column value on list actions. The first colon (:) in
                the parameter value delineates the column name or number from a regex selection pattern.
                Each row's column value is used with the regex pattern to determined row inclusion in the
                final result. By default, row is included if the regex pattern is found in the
                column value. The options parameter can be set to one or more of the following to modify
                the default behavior: literal - to treat the regex string as a literal string, exact -
                to require an exact match of the value (not just a find!), negative - to reverse the
                condition so a match means exclude the row. Row selection takes place after all other
                action specific filtering conditions including the limit determination and so generally
                should not be used with the limit parameter. (Optional)
        Examples:
            get_agent_capability()
            get_agent_capability(agent_name="@all")
            get_agent_capability(agent_name="zcapabilities")
            get_agent_capability(options="includeUnreferenced", regex=".*Maven.*")
        """
        command = str.format('--action getCapabilityList ')
        return self.add_optional_arguments(command, agent=agent_name, options=options,
                                           limit=limit, regex=regex, file=file_name,
                                           append=append, encoding=encoding, select=select)

    def send_command(self, function_name, **kwargs):
        try:
            # checking if the ACLI directory exists
            if os.path.exists(self.acli_directory_path):
                command = function_name(**kwargs)
                if os.sys.platform.startswith("linux"):
                    command = str.format("PATH={0}:$PATH && {0}/acli {1} {2}", self.acli_directory_path,
                                         self.bamboo_server_name, command)
                else:
                    command = str.format("cd {0} && acli {1} {2}", self.acli_directory_path, self.bamboo_server_name,
                                         command)
                reply = subprocess.check_output(command, shell=True)
                return reply
            else:
                raise FileNotFoundError("{0} folder does not exist!".format(self.acli_directory_path))
        except Exception as sender_exception:
            raise BambooException(sender_exception)
