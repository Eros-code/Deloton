import boto3
from botocore.exceptions import ClientError, WaiterError


class HRTNotifcation:
    def __init__(self):
        self.client = boto3.client('sns')
        self.topic_arn = 'arn:aws:sns:eu-west-2:605126261673:HRT-Email-Notification'

    def subscribe_sns(self, email_address:str):
        response = self.client.subscribe(
            TopicArn = self.topic_arn,
            Protocol = 'email',
            Endpoint = email_address,
            ReturnSubscriptionArn = True,
        )
        return response

    def send_notification(self,msg:str):
        self.client.publish(
            TopicArn=self.topic_arn,
            Message = msg
            )

def main():
    emailer = HRTNotifcation()
    emailer.send_notification('this is a test notification')

if __name__ == '__main__':
    main()