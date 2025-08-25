# Payment Integration Guide

## 🔧 Real Payment Integration Steps

### 1. Razorpay Integration (India)

```python
import razorpay

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_KEY_SECRET"))

def create_razorpay_order(amount, currency="INR"):
    """Create Razorpay order"""
    order_data = {
        "amount": amount * 100,  # Amount in paise
        "currency": currency,
        "receipt": f"order_{datetime.now().timestamp()}",
        "payment_capture": 1
    }
    
    order = razorpay_client.order.create(data=order_data)
    return order

def verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Verify payment signature"""
    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        return True
    except:
        return False
```

### 2. Stripe Integration (Global)

```python
import stripe

stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

def create_stripe_checkout_session(amount, success_url, cancel_url):
    """Create Stripe checkout session"""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Chatbot Subscription',
                },
                'unit_amount': amount * 100,  # Amount in paise
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session

def verify_stripe_webhook(payload, sig_header, endpoint_secret):
    """Verify Stripe webhook"""
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        return event
    except ValueError:
        return None
    except stripe.error.SignatureVerificationError:
        return None
```

## 🗄️ Database Schema (Optional)

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subscriptions table
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plan_name TEXT NOT NULL,
    plan_period TEXT NOT NULL,
    amount INTEGER NOT NULL,
    status TEXT DEFAULT 'active',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    payment_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Usage tracking table
CREATE TABLE usage_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    questions_asked INTEGER DEFAULT 0,
    date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🔒 Environment Variables

Create a `.env` file:

```
# Razorpay
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# Stripe
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

# Database
DATABASE_URL=sqlite:///chatbot.db

# Gemini API
GEMINI_API_KEY=your_gemini_api_key
```

## 📝 Implementation Notes

1. **Security**: Always validate payments on server-side
2. **Webhooks**: Use webhooks to handle payment confirmations
3. **Error Handling**: Implement proper error handling for failed payments
4. **Testing**: Use test keys during development
5. **Compliance**: Ensure PCI compliance for card data handling

## 🚀 Deployment Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Database**: Use PostgreSQL or MySQL for production
3. **Caching**: Implement Redis for session management
4. **Monitoring**: Add payment monitoring and alerts
5. **Backup**: Regular database backups

## 📞 Support Integration

For enterprise plans and custom requirements:
- Integrate with support ticket systems
- Add calendar booking for sales calls
- Email automation for follow-ups
