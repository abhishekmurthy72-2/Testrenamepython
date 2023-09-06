from CheckmarxPythonSDK.CxOne import (
    get_scm_orgs,
    get_org_repos,
    import_repo
)
from CheckmarxPythonSDK.CxOne.dto import (
    RepoScmImportInput,
    BranchInput
)

import logging

if __name__ == '__main__':

    scmOrgs = get_scm_orgs()
    scmRepos = get_org_repos("MGLcx")
#    for org in scmOrgs:
#        print(org.get("name"))
    for repo in scmRepos.repos:
        print(repo.fullName)
        repoInput = RepoScmImportInput(
            isRepoAdmin=repo.isRepoAdmin,
            id=repo.id,
            name=repo.name,
            branches =  BranchInput(name = repo.defaultBranch, isDefaultBranch = True),
            origin="Github",
            url=repo.url
        )
        #response=import_repo(repoInput, "MGLcx")
        #print(response)
