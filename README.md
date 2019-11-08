# jBot GitOps

Tooling to coordinate GitOps deployment flows.
Right now the only source code repository supported is AWS CodeCommit.
You must use AWS CodeBuild for building and deploying.

The tool will trigger on pull-requests to create temporary environments and will use S3 as the artifact repository.

Use code as an inspiration for you own tooling.
