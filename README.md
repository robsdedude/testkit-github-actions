# TestKit with GitHub Actions Demo

This repository is made to demonstrate how to set up 
[TestKit](https://github.com/neo4j-drivers/testkit) with GitHub Actions.

TestKit is a testing tool for [Neo4j](https://neo4j.com/) drivers. It's still
in an early development phase.

## Project Structure
The files in this project should be included in the driver's repository on root
level.
```
.
├── .github
│   └── workflows
│       └── testkit.yml  # GitHub actions configuration
├── testkit
│   ├── backend.py
│   ├── build.py
│   ├── Dockerfile
│   ├── integration.py
│   ├── stress.py
│   └── unittests.py
├── testkitbackend
│   └── …
├── .testkit_version
└── … # the actual driver code
```

### `testkit` Folder
This folder contains files that TestKit needs to build and run the driver and
the backend. This folder is called "glue". The filenames and the folder's name
mustn't be altered as TestKit expects the glue to follow this pattern.
The files in `./testkit` each contain a few lines at the top that describe what
they're good for. Here's an even shorter summary:
 - `backend.py` start the TestKit backend.
 - `build.py` build the driver and the TestKit backend.
 - `Dockerfile` a [dockerfile](https://docs.docker.com/engine/reference/builder/)
   that provides everythin needed to run the driver and the TestKit backend.
 - `integration.py` run additional integration tests.
 - `stress.py` run additional stress tests.  
   Note: currently, TestKit comes with no stress tests. So "additional" at the
   time of writing this means "any". Stress tests in TestKit are planned for the
   future.
 - `unittests.py` run unittests.

### `testkitbackend` Folder
This folder could have any other name (requires adjustment of 
`.testkit/backend.py`)  

It contains a backend implementation that's typically written in the driver's
native language. The backend communicates with TestKit via a socket and
translates received instructions into native driver calls.  
In this specific repository the backend is a mock and does not use an actual
driver.

### `.testkit_version`
This file contains the TestKit version (commit hash, branch, …) that should be
used to test the driver. We highly recommend fixing TestKit to a commit hash
to avoid unexpected breaking of you CI when TestKit receives an update. This
way you can update the used TestKit version at your onwn pace.
