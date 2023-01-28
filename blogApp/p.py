import stripe
stripe.api_key = "sk_test_51MSzBNIO3w4jgP1a1Z6kUnzLDntWylMrr6uBU7gT2ek94TFL6JJ95gvBe2hBCcYFyeWMaJULbKGcMSj7tNw59wkO00xp6Xcuim"

s = stripe.Account.create(
    type="custom",
    email="jens.db@example.com",
    capabilities={
        "card_payments": {"requested": True},
        "transfers": {"requested": True},
    },
    business_type="individual"
)


# link = stripe.AccountLink.create(
#     account=s['id'],
#     refresh_url="http://localhost:8000/",
#     return_url="http://localhost:8000/courses",
#     type="account_onboarding",
#     collect="currently_due"
# )

print(s)
print(s['id'])
# print(link)
# print(link['url'])

# t = stripe.Transfer.create(
#   amount=400,
#   currency="usd",
#   destination="acct_1MUTEdI3RJ8pJ4XN",
# )


# print(t)


# print(stripe.Balance.retrieve())








































