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

def accept_policy():
    current_timestamp = int(time.time())  # Get current time as Unix timestamp
    policy_update = stripe.issuing.Cardholder.modify(
        os.getenv("CARDHOLDER_ID"),
        individual={
            "card_issuing": {
                "user_terms_acceptance": {
                    "date": current_timestamp,
                    
                },
            },
        },
    )

    print(policy_update)

# accept_policy()


# activate user card for transaction 
def update_card_status():
    activate= stripe.issuing.Card.modify(
  os.getenv("CARD_ID"),
  status="active",
)
    
    
# update_card_status()

def test_payment():
    
 authorization= stripe.issuing.Authorization.TestHelpers.create(
  amount=100,
  card=os.getenv("CARD_ID"),
)
 
 authorize_payment= stripe.issuing.Authorization.TestHelpers.capture(authorization.id)

 print(authorize_payment);



