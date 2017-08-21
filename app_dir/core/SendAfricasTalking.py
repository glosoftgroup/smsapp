# Import the helper gateway class
from app_dir.core.AfricasTalkingGateway import AfricasTalkingGateway, \
    AfricasTalkingGatewayException

# Specify your login credentials
username = "mercy@glosoftgroup.com"
apikey = "f6ad8ebb434514af8a90f961bf38e0bbb71659b26981cb38914c4941a5862041"

# NOTE: If connecting to the sandbox, please use your sandbox login credentials

# Specify the numbers that you want to send to in a comma-separated list
# Please ensure you include the country code (+254 for Kenya)
to = "+254711727778,+254715690530"

# And of course we want our recipients to know what we really do
message = "This is a Test message from smsapp via AfricasTalking"

# Create a new instance of our awesome gateway class
gateway = AfricasTalkingGateway(username, apikey, "sandbox")

# NOTE: If connecting to the sandbox, please add the sandbox flag to the constructor:
# *************************************************************************************
#             ****SANDBOX****
# gateway    = AfricasTalkingGateway(username, apiKey, "sandbox");
# **************************************************************************************

# Any gateway errors will be captured by our custom Exception class below,
# so wrap the call in a try-catch block
try:
    # Thats it, hit send and we'll take care of the rest.

    results = gateway.sendMessage(to, message)

    for recipient in results:
        # status is either "Success" or "error message"
        print 'number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                            recipient['status'],
                                                            recipient['messageId'],
                                                            recipient['cost'])
except AfricasTalkingGatewayException, e:
    print 'Encountered an error while sending: %s' % str(e)

