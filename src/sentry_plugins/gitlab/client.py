from __future__ import absolute_import

from gitlab import Gitlab
from gitlab.exceptions import GitlabGetError, GitlabAuthenticationError, GitlabCreateError

from sentry_plugins.exceptions import ApiError


class GitLabClient(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.gl = Gitlab(url, private_token=self.token)
        self.auth()

    def auth(self):
        try:
            return self.gl.auth()
        except GitlabAuthenticationError as e:
            raise ApiError('Not authorized to access GitLab instance', e.response_code)

    def get_project(self, repo):
        try:
            return self.gl.projects.get(repo).attributes
        except GitlabGetError as e:
            raise ApiError('Project not found with name', e.response_code)

    def get_issue(self, repo, issue_id):
        try:
            return self.gl.projects.get(repo).issues.get(issue_id).attributes
        except GitlabGetError as e:
            raise ApiError('Issue not found with ID', e.response_code)

    def create_issue(self, repo, data):
        try:
            issue = self.gl.projects.get(repo).issues.create(data)
            return issue.attributes
        except GitlabCreateError as e:
            raise ApiError('Could not create issue', e.response_code)

    def create_note(self, repo, issue_iid, data):
        try:
            note = self.gl.projects.get(repo).issues\
                .get(issue_iid).notes.create(data)
            return note.attributes
        except GitlabCreateError as e:
            raise ApiError('Could not create note', e.response_code)

    def list_project_members(self, repo):
        return [
            member.attributes for member in
            self.gl.projects.get(repo).members.list(all=True)
        ]
