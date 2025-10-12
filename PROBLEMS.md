Run actions/checkout@v5
  with:
    repository: IAmJonoBo/Agentic-Canon
    token: ***
    ssh-strict: true
    ssh-user: git
    persist-credentials: true
    clean: true
    sparse-checkout-cone-mode: true
    fetch-depth: 1
    fetch-tags: false
    show-progress: true
    lfs: false
    submodules: false
    set-safe-directory: true
Syncing repository: IAmJonoBo/Agentic-Canon
Getting Git version info
Temporarily overriding HOME='/home/runner/work/_temp/34476265-7a16-4c27-a06e-942bb24fff56' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/Agentic-Canon/Agentic-Canon
Deleting the contents of '/home/runner/work/Agentic-Canon/Agentic-Canon'
Initializing the repository
  /usr/bin/git init /home/runner/work/Agentic-Canon/Agentic-Canon
  hint: Using 'master' as the name for the initial branch. This default branch name
  hint: is subject to change. To configure the initial branch name to use in all
  hint: of your new repositories, which will suppress this warning, call:
  hint:
  hint: 	git config --global init.defaultBranch <name>
  hint:
  hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
  hint: 'development'. The just-created branch can be renamed via this command:
  hint:
  hint: 	git branch -m <name>
  hint:
  hint: Disable this message with "git config set advice.defaultBranchName false"
  Initialized empty Git repository in /home/runner/work/Agentic-Canon/Agentic-Canon/.git/
  /usr/bin/git remote add origin https://github.com/IAmJonoBo/Agentic-Canon
Disabling automatic garbage collection
  /usr/bin/git config --local gc.auto 0
Setting up auth
  /usr/bin/git config --local --name-only --get-regexp core\.sshCommand
  /usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
  /usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
  /usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
  /usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
Fetching the repository
  /usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +03d82ffc38edb8e15f0fbb9d8a40df74c402781b:refs/remotes/pull/86/merge
  remote: Repository not found.
  Error: fatal: repository 'https://github.com/IAmJonoBo/Agentic-Canon/' not found
  The process '/usr/bin/git' failed with exit code 128
  Waiting 19 seconds before trying again
  /usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +03d82ffc38edb8e15f0fbb9d8a40df74c402781b:refs/remotes/pull/86/merge
  remote: Repository not found.
  Error: fatal: repository 'https://github.com/IAmJonoBo/Agentic-Canon/' not found
  The process '/usr/bin/git' failed with exit code 128
  Waiting 12 seconds before trying again
  /usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +03d82ffc38edb8e15f0fbb9d8a40df74c402781b:refs/remotes/pull/86/merge
  remote: Repository not found.
  Error: fatal: repository 'https://github.com/IAmJonoBo/Agentic-Canon/' not found
  Error: The process '/usr/bin/git' failed with exit code 128
