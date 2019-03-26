#!/usr/bin/python

# Copyright: (c) 2019, Nathan Kinder <nkinder@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: certmonger_getcert

short_description: Manage SSL/TLS certificates via certmonger

version_added: "2.8"

description:
    - "Request and manage the renewal tracking of SSL/TLS certificates via
      "the certmonger daemon."

options:
    # NGK(TODO) - add nss DB options
    key:
        description:
            - "Path to the PEM file for the private key."
    cert:
        description:
            - "Path to the PEM file for the certificate (only valid when
               using the C(key) option)."
    password:
        description:
            - "Password for key encryption."
    password_file:
        description:
            - "File containing password for key encryption."
    ca:
        description:
            - "The CA to request the certificate from (as defined in
               certmonger).  The C(local) CA will use certmonger's local
               self-signed CA.  The C(IPA) CA will request a certificate from
               a FreeIPA CA on a system that is enrolled as a FreeIPA client."
        default: 'local'
    # NGK(TODO) - add CA profile/issuer options
    nickname:
        description:
            - "Nickname of the certificate request."
    # NGK(TODO) - add CSR options (cert subject/fields)
    subject:
        description:
            - "Requested certificate subject name (default: CN=<hostname>)."
    principal:
        description:
            - "Set requested principal name in the CSR.  This is required when
              "requesting a certificate from the C(IPA) CA."
    # NGK(TODO) - add key type/size options
    renew:
        description:
            - "Attempt to renew the certificate when expiration nears."
        type: bool
        default: 'yes'
    # NGK(TODO) - add pre/post save options
    wait:
        description:
            - "Try to wait for the certificate to be issued."
        type: bool
        defaut: 'yes'
    # NGK(TODO) - add state (present, absent, resubmitted).  Present should request
    # if the cert/key doesn't exist.  If it does exist, ensure it is being
    # tracked.  If it is tracked and not issued, resubmit.  Absent will just
    # remove tracking, but it will leave the files.
    state:
        description:
            - "NGK(TODO) - add description"
        default: 'present'

author:
    - Nathan Kinder (@nkinder)
'''

EXAMPLES = '''
# Request a certificate (local CA)
- name: Request a certificate from the local self-signed CA
  certmonger_getcert:
    key: /path/to/server.key
    cert: /path/to/server.pem
    nickname: server

# Request a certificate (IPA)
- name: Request a certificate from the local self-signed CA
  certmonger_getcert:
    key: /path/to/server.key
    cert: /path/to/server.pem
    ca: IPA
    nickname: server
    subject: CN=server.example.test,O=EXAMPLE.TEST
    principal: http/server.example.test

# Resubmit a certificate request

# Get status of a cert (just use return value?)

# Start tracking

# Stop tracking

# refresh cas

# list operations?
'''

# NGK(TODO) - Add returns details.  We should expose everything you would see in the
# 'status' output from getcert.
RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

import socket

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        # NGK(TODO) - initialize state here
        #original_message='',
        #message=''
    )

    module = AnsibleModule(
        argument_spec=dict(
            nss_db=dict(type='str', required=False),
            nss_nickname=dict('str', required=False),
            nss_token=dict=('str', required=False),
            key=dict(type='str', required=False),
            cert=dict(type='str', required=False),
            password=dict(type='str', required=False),
            password_file=dict(type='str', required=False, no_log=True),
            ca=dict(type='str', required=False, default='local'),
            nickname=dict(type='str', required=False),
            subject=dict(type='str', required=False, default='CN={0}'.format(socket.gethostname())),
            principal=dict(type='str', required=False),
            renew=dict(type='bool', required=False, default=True),
            wait=dict(type='bool', required=False, default=True),
            state=dict(type='str', choices=['present', 'absent', 'resubmitted'], required=False, default='present')
        ),
        required_one_of=(
            ['key', 'nss_db'],
        ),
        required_together=(
            ['key', 'cert'],
            ['nss_db', 'nss_nickname'],
        ),
        required_if=[
            [ 'ca', 'IPA', [ 'principal' ] ],
            # NGK(TODO) - absent and present rules will probably be useful
            # [ "state", "present", [ "a", "b" ] ],
            # [ "state", "absent", [ "a" ] ]
        ],
        mutually_exclusive=(
            ['key', 'nss_db'],
            ['password', 'password_file'],
        ),
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    #result['original_message'] = module.params['name']
    #result['message'] = 'goodbye'

    # NGK(TODO) - call certmonger here with key, cert, ca, nickname, subject, renew, and wait

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    #if module.params['new']:
    #    result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if module.params['name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
