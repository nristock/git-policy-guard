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

## Policies
### FileBlacklist
Checks all names of changed files against a list of regex pattern. If a single pattern matches, the ref update will be rejected.  
#### Parameters
* blacklist_pattern (list\[str\]): A list of regex pattern to check for.
