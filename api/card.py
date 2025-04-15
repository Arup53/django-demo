from dotenv import load_dotenv
import stripe
import os
import time

load_dotenv() 

stripe.api_key = os.getenv("STRIPE_TEST_API_KEY")

# Create cardholder and card
def create_cardholder():
    cardholder = stripe.issuing.Cardholder.create(
    name="goi",
    email="goikoi@example.com",
    phone_number="+18008675309",
    status="active",
    type="individual",
    individual={
    "first_name": "Jenny",
    "last_name": "Rosen",
    "dob": {"day": 1, "month": 11, "year": 1981},
  },
  billing={
    "address": {
      "line1": "123 Main Street",
      "city": "San Francisco",
      "state": "CA",
      "postal_code": "94111",
      "country": "US",
    },
  }, 
)
    
    card= stripe.issuing.Card.create(
  cardholder=cardholder.id,
  currency="usd",
  type="virtual",
)
    return {
        "cardholderId": cardholder.id,
        "cardId": card.id,
    }
    



# result = create_cardholder()
# print(result)

# accept policy for user

def accept_policy(cardHolderId, cardId):
    current_timestamp = int(time.time())  # Get current time as Unix timestamp
    policy_update = stripe.issuing.Cardholder.modify(
        cardHolderId,
        individual={
            "card_issuing": {
                "user_terms_acceptance": {
                    "date": current_timestamp,
                    
                },
            },
        },
    )
    activate= stripe.issuing.Card.modify(cardId,status="active")

    print(policy_update)
    

# accept_policy()


# activate user card for transaction 
# def update_card_status():
#     activate= stripe.issuing.Card.modify(
#   os.getenv("CARD_ID"),
#   status="active",
# )
    
    
# update_card_status()




def pay_with_virtual_card(card_id, amount):
    try:
        authorization= stripe.issuing.Authorization.TestHelpers.create(
           amount=amount,
           card=card_id,
        )
        authorize_payment= stripe.issuing.Authorization.TestHelpers.capture(authorization.id)
        
        print(authorize_payment);
        return {"approved": True}
    except Exception as e:
        print("Stripe error:", str(e))
        return {"approved": False, "error": str(e)}

