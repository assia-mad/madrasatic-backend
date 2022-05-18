from django.conf import settings
from pusher_push_notifications import PushNotifications
import pusher 


"""
Notification push with pusher Beams
"""
def push_notify(user_id, responsable_id, title, body):

        push_client = PushNotifications(

                instance_id='4a4e8ca8-c1da-42b3-bace-da94c8f6c095',
                secret_key='51667486C8B2797CCF1B8FA4358326C1DD1B3307B15A3D916369ECFFB160ACD5',
        )
        response = push_client.publish_to_users(
                user_ids = [str(user_id), str(responsable_id)],
                publish_body={

                        'apns': {

                                'aps': {
                                'alert': title,
                                },
                                },
                        'fcm': {

                                'notification': {
                                'title': title,
                                'body': body,
                                },
                        },
                },
            )
        print(response['publishId'])

"""
Notification push with pusher channels
"""
def channels_notify(channel, event, data):

        pusher_client = pusher.Pusher(
                app_id= settings.PUSHER_APP_ID,
                key= settings.PUSHER_KEY,
                secret= settings.PUSHER_SECRET,
                cluster= settings.PUSHER_CLUSTER ,
                ssl=True
                )
        return pusher_client.trigger(channel, event, {u'message': data})
