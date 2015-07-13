# Sample Python AWS API demonstration script
# --Ashay Chitnis, 12/07/2015

import sys
from datetime import datetime
from boto3.session import Session

def sys_exit(val):
    print('Exiting...')
    sys.exit(val)

class DemoEc2(object):
    """
    """
    def __init__(self, client):
        """
        :param client:
        """
        self.client = client
        self.dry_run = False

    def create_aws_spot_fleet(self):
        """
        :return: resp
        """
        # pre-configured dictionary of desired instance configuration,
        # one can automate it to receive inputs from CLI or a Web interface

        request_config = {
            "TargetCapacity": 3,
            "SpotPrice": "0.012",
            "IamFleetRole": "arn:aws:iam::547078464708:role/ck_spot_fleet_role",
            "LaunchSpecifications": [
                {
                    "ImageId": "ami-e7539d8c",
                    "InstanceType": "t1.micro",
                    "SubnetId": "subnet-e9cfd8d3"
                }
            ]
        }
        resp = self.client.request_spot_fleet(
            DryRun=self.dry_run,
            SpotFleetRequestConfig=request_config,
        )
        return resp

    def history_aws_spot_fleet(self, spot_fleet_id=''):
        """
        :return: resp
        """
        resp = self.client.describe_spot_fleet_request_history(
            DryRun=self.dry_run,
            SpotFleetRequestId=spot_fleet_id,
            StartTime=datetime(2015, 7, 12),
        )
        return resp

    def describe_aws_spot_fleet(self, spot_fleet_id=''):
        """
        :return: resp
        """
        resp = self.client.describe_spot_fleet_instances(
            DryRun=self.dry_run,
            SpotFleetRequestId=spot_fleet_id,
        )
        return resp

    def terminate_aws_spot_fleet(self, spot_fleet_id=''):
        """
        :return: resp
        """
        resp = self.client.cancel_spot_fleet_requests(
            DryRun=self.dry_run,
            SpotFleetRequestIds=[
                spot_fleet_id,
            ],
            TerminateInstances=True
        )
        return resp


def main():
    if len(sys.argv) != 3:
        sys_exit(1)

    if (sys.argv[1] == 'start' or sys.argv[1] == 'history' or sys.argv[1] == 'show' or sys.argv[1] == 'stop') is False:
        sys_exit(1)

    default_profile='aater-flux7'
    spot_fleet_id = sys.argv[2]
    session = Session(profile_name=default_profile)
    client = session.client('ec2')
    resource = DemoEc2(client)
    ret = False

    if sys.argv[1] == 'start':
        ret = resource.create_aws_spot_fleet()
    elif sys.argv[1] == 'show':
        ret = resource.describe_aws_spot_fleet(spot_fleet_id)
    elif sys.argv[1] == 'history':
        ret = resource.history_aws_spot_fleet(spot_fleet_id)
    elif sys.argv[1] == 'stop':
        ret = resource.terminate_aws_spot_fleet(spot_fleet_id)

    print ret

if __name__ == '__main__':
    main()
