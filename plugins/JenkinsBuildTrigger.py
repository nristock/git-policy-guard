from http.client import HTTPConnection
import re
from urllib.parse import urlparse

from Logging import get_main_logger
from Plugin import Plugin
from Utils import GitRev, GitReference


class JenkinsBuildTrigger(Plugin):
    _PARAMETER_INTERPOLATION_LAMBDAS = {
        '$REF_NAME': lambda build_trigger_instance: build_trigger_instance.current_ref.name
    }

    def __init__(self, jenkins_base_url, job_name, ref_to_trigger_on, build_parameters=None):
        self.jenkins_base_url = jenkins_base_url
        self.job_name = job_name
        self.ref_to_trigger_on = re.compile(ref_to_trigger_on)
        self.build_parameters = build_parameters

        self.current_ref = None

    def generate_url(self):
        if self.build_parameters:
            return '{0}/job/{1}/buildWithParameters'.format(self.jenkins_base_url, self.job_name)
        else:
            return '{0}/job/{1}/build'.format(self.jenkins_base_url, self.job_name)

    def interpolate_build_parameters(self):
        if not self.build_parameters:
            return ''

        params = []
        for key, value in self.build_parameters.items():
            params += ['{0}={1}'.format(key, self.interpolate_parameter(value))]

        return '&'.join(params)

    def interpolate_parameter(self, interpolation_token):
        if not interpolation_token.startswith("$"):
            return interpolation_token

        stripped_token = interpolation_token.strip()
        assert JenkinsBuildTrigger._PARAMETER_INTERPOLATION_LAMBDAS.__contains__(stripped_token)
        return JenkinsBuildTrigger._PARAMETER_INTERPOLATION_LAMBDAS[stripped_token](self)

    def post_receive(self, received_refs):
        for ref in received_refs:
            self.process_ref(ref)

    def process_ref(self, ref):
        if self.ref_to_trigger_on.match(ref.ref_name):
            # Check for branch delete (xxxxx -> 000000)
            if GitRev(ref.new_rev).is_null_rev():
                return

            self.current_ref = GitReference(ref.ref_name)

            trigger_url = self.generate_url()
            parsed_url = urlparse(trigger_url)

            trigger_path = '{0}?{1}'.format(parsed_url.path, self.interpolate_build_parameters())
            get_main_logger().info("Triggering Jenkins build {0}".format(trigger_path))

            connection = HTTPConnection(parsed_url.hostname, parsed_url.port)
            connection.request("GET", trigger_path)
            connection.close()
