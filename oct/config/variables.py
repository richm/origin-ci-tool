# coding=utf-8
from __future__ import absolute_import, division, print_function

DEFAULT_ESCALATION_METHOD = 'sudo'
DEFAULT_USER = 'origin'
DEFAULT_TARGET_GROUP = 'OSEv3'
DEFAULT_CONNECTION_METHOD = 'ssh'
DEFAULT_DOCKER_VOLUME_GROUP = 'docker'


class PlaybookExtraVariables(object):
    """
    This container holds values for defaulting
    the set of extra variables that we set for
    playbook execution.

    Every member field of this class will become
    an extra var named 'origin_ci_' + field_name.
    """

    def __init__(
            self,
            # host configuration
            target_hosts=DEFAULT_TARGET_GROUP,
            connection_method=DEFAULT_CONNECTION_METHOD,
            # remote user configuration
            become=True,
            become_method=DEFAULT_ESCALATION_METHOD,
            become_user=DEFAULT_USER,
            # miscellaneous variables
            docker_volume_group=DEFAULT_DOCKER_VOLUME_GROUP,
    ):
        # hosts to target for the following plays
        self.hosts = target_hosts
        # method for connecting to the target hosts
        self.connection = connection_method

        # whether or not to change into a user on the remote host
        self.become = become
        # method to use for privilege escalation on the remote host
        self.become_method = become_method
        # user to become on the remote host, for which we need to
        # set both the `become_user` and `user` vars as they are
        # contextually independent
        self.become_user = become_user
        self.user = become_user

        # volume group to use for Docker storage on the remote host
        self.docker_volume_group = docker_volume_group

    def __iter__(self):
        """
        Return an iterator for contained properties.

        :return: the iterator
        """
        return (x for x in vars(self))

    def __getitem__(self, key):
        """
        Fetch the configuration key.

        :param key: name of the item to fetch
        :return: value of the item
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError('No such option `{}`.'.format(key))

    def __setitem__(self, key, value):
        """
        Update the value of the configuration entry.

        :param key: name of the item to update
        :param value: value to update the item to
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError('No such option `{}`.'.format(key))

    def __contains__(self, key):
        """
        Determine if the container in fact
        contain the configuration item.

        :param key: name of the item to search for
        :return: whether or not we contain the item
        """
        return hasattr(self, key)

    def default(self, playbook_variables=None):
        """
        Default unset values in the Ansible extra playbook
        variables using values loaded from serialized or
        default configurations. We do *not* default values
        that are `None' as these can be valid user choices.

        :param playbook_variables: partially-filled variables
        :return: defaulted Ansible extra playbook variables
        """
        if playbook_variables is None:
            playbook_variables = {}

        for field in self.__dict__:
            variable = 'origin_ci_{}'.format(field)
            if variable not in playbook_variables:
                playbook_variables[variable] = self.__dict__[field]

        return playbook_variables
