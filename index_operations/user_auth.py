import boto3
import jwt

class userAuthentication(object):
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.user_table = dynamodb.Table('words_users')
        self.secret = 'egg_grab' #TODO: Get this to a more secure place

    def create_user(self, email, first_name, last_name, phone_number=None):
        response = self.user_table.put_item(
            Item = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
            }
        )
        return response

    def login(self, email, password):
        token = self.generate_token(
            {"email":email, "password":password}, 
            self.secret, 
            "HS256"
            )
        #No idea really how this stuff works yet,
        #I'm just kinda making things I think we need
        
    
    def generate_token(self, payload, secret, algorithm):
        token = jwt.encode(payload, secret, algorithm=algorithm)
        return token

    def update_password(self):
        pass