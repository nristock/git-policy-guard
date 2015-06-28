## Setup
0. Make sure you have python3 installed
1. cd into the repository's hooks directory: `cd /my/bare/repo/hooks`
2. Clone the project: `git clone https://github.com/Monofraps/git-policy-guard.git`
3. Run the setup script `git-policy-guard/setup-repo.py` 
4. Create a config file called `settings.py` (you can copy `settings.py.sample`)

## Plugins
### PolicyCheck
Applies a list of policies before a ref gets updated and rejects the update if a single policy check fails.
#### Parameters
* policies (list\[Policy\]): The policies to apply

### JenkinsBuildTrigger
Triggers a jenkins build on the specified project if the specified ref filter matches one of the pushed refs. This plugin can pass parameters to the build job.
### Parameters
* jenkins_base_url (str): The base URl of the Jenkins server (e.g. `http://10.0.1.23:8081`).
* job_name (str): The job to trigger.
* ref_to_trigger_on (str/regex): Regex on which to trigger `job_name` (e.g. `refs/tags/.*` to trigger every time a tag is pushed).
* build_parameters (map\[str -> str\]): Map of parameters to pass to the build job (e.g. `{'branch_name': '$REF_NAME'}` will pass the pushed ref's name as `branch_name` to the build) Check `JenkinsBuildTrigger._PARAMETER_INTERPOLATION_LAMBDAS` for available placeholders. 

## Policies
### FileBlacklist
Checks all names of changed files against a list of regex pattern. If a single pattern matches, the ref update will be rejected.  
#### Parameters
* blacklist_pattern (list\[str\]): A list of regex pattern to check for.

### NoEmptyCommitMessage
Rejects the ref update if an empty (as in no non-whitespace character) commit message is found.
