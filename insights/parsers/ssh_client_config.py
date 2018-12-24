"""
SshConfig - file for ``ssh client config``
==========================================

This module contains parsers that check the ssh client config files.

Parsers provided by this module are:

EtcSshConfig - file ``/etc/ssh/ssh_config``
-------------------------------------------

ForemanSshConfig - file ``/usr/share/foreman/.ssh/ssh_config``
--------------------------------------------------------------

"""
from collections import namedtuple

from insights.specs import Specs

from .. import Parser, get_active_lines, parser


class SshClientConfig(Parser):
    """Base class for sshclient config file."""

    KeyValue = namedtuple('KeyValue', ['keyword', 'value', 'line'])

    def parse_content(self, content):
        self.global_lines = []
        self.host_lines = {}

        _content = get_active_lines(content)
        index_list = [i for i, l in enumerate(_content) if l.startswith('Host ')]
        index = index_list[0] if index_list else len(_content)

        for line in _content[:index]:
            line_splits = [s.strip() for s in line.split(None, 1)]
            kw, val = line_splits[0], line_splits[1] if len(line_splits) == 2 else ''
            self.global_lines.append(self.KeyValue(kw, val, line))

        hostbit = ''
        for line in _content[index:]:
            line_splits = [s.strip() for s in line.split(None, 1)]
            kw, val = line_splits[0], line_splits[1] if len(line_splits) == 2 else ''
            if kw == 'Host':
                hostbit = kw + '_' + val
                self.host_lines[hostbit] = []
            else:
                self.host_lines[hostbit].append(self.KeyValue(kw, val, line))


@parser(Specs.ssh_config)
class EtcSshConfig(SshClientConfig):
    """
    This parser reads the file ``/etc/ssh/ssh_config``

    Sample output::

        #   ProxyCommand ssh -q -W %h:%p gateway.example.com
        #   RekeyLimit 1G 1h
        #
        # Uncomment this if you want to use .local domain
        # Host *.local
        #   CheckHostIP no
        ProxyCommand ssh -q -W %h:%p gateway.example.com

        Host *
            GSSAPIAuthentication yes
        # If this option is set to yes then remote X11 clients will have full access
        # to the original X11 display. As virtually no X11 client supports the untrusted
        # mode correctly we set this to yes.
            ForwardX11Trusted yes
        # Send locale-related environment variables
            SendEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES
            SendEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
            SendEnv LC_IDENTIFICATION LC_ALL LANGUAGE
            SendEnv XMODIFIERS

        Host proxytest
            HostName 192.168.122.2

    Attributes:

        global_lines (list): The list of site-wide configuration, as
            namedtuple('KeyValue', ['keyword', 'value', 'line']).
        host_lines (dict): The dict of all host-specific definitions, as
            {'Host_name': [namedtuple('KeyValue', ['keyword', 'value', 'line'])]}

    Examples:
        >>> len(etcsshconfig.global_lines)
        1
        >>> etcsshconfig.global_lines[0].keyword
        'ProxyCommand'
        >>> etcsshconfig.global_lines[0].value
        'ssh -q -W %h:%p gateway.example.com'
        >>> 'Host_*' in etcsshconfig.host_lines
        True
        >>> etcsshconfig.host_lines['Host_*'][0].keyword
        'GSSAPIAuthentication'
        >>> etcsshconfig.host_lines['Host_*'][0].value
        'yes'
        >>> etcsshconfig.host_lines['Host_*'][1].keyword
        'ForwardX11Trusted'
        >>> etcsshconfig.host_lines['Host_*'][1].value
        'yes'
        >>> etcsshconfig.host_lines['Host_proxytest'][0].keyword
        'HostName'
        >>> etcsshconfig.host_lines['Host_proxytest'][0].value
        '192.168.122.2'
    """
    pass


@parser(Specs.ssh_foreman_config)
class ForemanSshConfig(SshClientConfig):
    """
    This parser reads the file ``/usr/share/foreman/.ssh/ssh_config``

    Sample output::

        #   ProxyCommand ssh -q -W %h:%p gateway.example.com
        #   RekeyLimit 1G 1h
        #
        # Uncomment this if you want to use .local domain
        # Host *.local
        #   CheckHostIP no
        ProxyCommand ssh -q -W %h:%p gateway.example.com

        Host *
            GSSAPIAuthentication yes
        # If this option is set to yes then remote X11 clients will have full access
        # to the original X11 display. As virtually no X11 client supports the untrusted
        # mode correctly we set this to yes.
            ForwardX11Trusted yes
        # Send locale-related environment variables
            SendEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES
            SendEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
            SendEnv LC_IDENTIFICATION LC_ALL LANGUAGE
            SendEnv XMODIFIERS

        Host proxytest
            HostName 192.168.122.2

    Attributes:

        global_lines (list): The list of site-wide configuration, as
            namedtuple('KeyValue', ['keyword', 'value', 'line']).
        host_lines (dict): The dict of all host-specific definitions, as
            {'Host_name': [namedtuple('KeyValue', ['keyword', 'value', 'line'])]}

    Examples:
        >>> len(foremansshconfig.global_lines)
        1
        >>> foremansshconfig.global_lines[0].keyword
        'ProxyCommand'
        >>> foremansshconfig.global_lines[0].value
        'ssh -q -W %h:%p gateway.example.com'
        >>> 'Host_*' in foremansshconfig.host_lines
        True
        >>> foremansshconfig.host_lines['Host_*'][0].keyword
        'GSSAPIAuthentication'
        >>> foremansshconfig.host_lines['Host_*'][0].value
        'yes'
        >>> foremansshconfig.host_lines['Host_*'][1].keyword
        'ForwardX11Trusted'
        >>> foremansshconfig.host_lines['Host_*'][1].value
        'yes'
        >>> foremansshconfig.host_lines['Host_proxytest'][0].keyword
        'HostName'
        >>> foremansshconfig.host_lines['Host_proxytest'][0].value
        '192.168.122.2'
    """
    pass