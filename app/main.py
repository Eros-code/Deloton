import boto3
from botocore.exceptions import ClientError, WaiterError

import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException

# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = 'elizabeth_astra_minerva'
configuration.password = '155DAEE4-59BD-F47A-8426-848B33FA3177'

# create an instance of the API class
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

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
    
    def check_heart_rate(self, heart_rate:int, age:int):
        age_in = lambda min, max: age > min or age < max 
        
        max_heart_rate = 0
        DANGEROUS_HEART_RATE = 250
        
        if heart_rate > DANGEROUS_HEART_RATE:
            self.send_emergency_notification()
    
        match age:
            case age_in(20, 29):
                max_heart_rate = 200
            case age_in(30, 34):
                max_heart_rate = 190
            case age_in(35, 39):
                max_heart_rate = 185
            case age_in(40, 44):
                max_heart_rate = 180
            case age_in(45, 49):
                max_heart_rate = 175
            case age_in(50, 54):
                max_heart_rate = 170
            case age_in(55, 59):
                max_heart_rate = 165
            case age_in(60, 64):
                max_heart_rate = 160
            case age_in(65, 69):
                max_heart_rate = 155
            case age_in(70, 79):
                max_heart_rate = 150
            case _:
                max_heart_rate = 140
        
        if heart_rate > max_heart_rate:
            return True
        
        return False
                
    def send_emergency_notification(self):
        # If you want to explictly set from, add the key _from to the message.
        sms_message = SmsMessage(
            body="Heart Rate exceeded Dangerous Levels, a rider has died lmao",
            to="+447833948642"
        )

        sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])
        #TODO: Send emergency notification, eg: phone call or SMS text
        try:
            # Send sms message(s)
            api_response = api_instance.sms_send_post(sms_messages)
            print(api_response)
        except ApiException as e:
            print("Exception when calling SMSApi->sms_send_post: %s\n" % e)


def main():
    notifier = HRTNotifcation()
    # notifier.send_notification('this is a test notification')
    notifier.send_emergency_notification()

if __name__ == '__main__':
    main()