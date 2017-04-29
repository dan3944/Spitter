from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACc4bd56b82a463f76094cf22dfcc0e7a3"
auth_token = "01a0ecc27726f2f049d6d9318bcc7bfd"
client = Client(account_sid, auth_token)

call = client.calls.create(to="+16179224633",
                           from_="+16172497143",
                           url="http://demo.twilio.com/docs/voice.xml")

print(call.sid)