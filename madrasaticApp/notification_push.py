from django.conf import settings
from pusher_push_notifications import PushNotifications
import pusher 


"""
Notification push with pusher Beams
"""
def push_notify(user_id, responsable_id, title, body):

        push_client = PushNotifications(

                instance_id='07664670-9ac3-47fb-b92f-1f54942f1d20',
                secret_key='77D48F249287CAEFC9700E12DA6C8984DC2F37972BCBEE62D45528ECDE3F5B65',
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
