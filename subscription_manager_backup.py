import streamlit as st
import json
import datetime
from typing import Dict, Optional

class SubscriptionManager:
    """Manages subscription plans, limits, and payment integration."""
    
    def __init__(self):
        self.plans = {
            "explorer": {
                "name": "Explorer",
                "features": [
                    "1 User",
                    "Import Module",
                    "Basic Dashboard Only"
                ],
                "limits": {
                    "questions_per_day": 10,
                    "documents": 1,
                    "users": 1
                },
                "pricing": {
                    "weekly": 99,
                    "monthly": 299,
                    "quarterly": 749,
                    "yearly": 2499
                }
            },
            "starter": {
                "name": "Starter",
                "features": [
                    "🔹 1 User",
                    "🔹 Import & Export Modules",
                    "🔹 Email Support"
                ],
                "limits": {
                    "questions_per_day": 50,
                    "documents": 5,
                    "users": 1
                },
                "pricing": {
                    "weekly": 199,
                    "monthly": 499,
                    "quarterly": 1299,
                    "yearly": 4499
                }
            },
            "professional": {
                "name": "Professional",
                "features": [
                    "🔹 2 Users",
                    "🔹 Import/Export + Trade Benefits",
                    "🔹 Email Support",
                    "🔹 Basic Reports"
                ],
                "limits": {
                    "questions_per_day": 100,
                    "documents": 10,
                    "users": 2
                },
                "pricing": {
                    "weekly": 299,
                    "monthly": 799,
                    "quarterly": 2099,
                    "yearly": 7499
                }
            },
            "advanced": {
                "name": "Advanced",
                "features": [
                    "🔹 3 Users",
                    "🔹 All Modules",
                    "🔹 Monthly Compliance Reports",
                    "🔹 Priority Support"
                ],
                "limits": {
                    "questions_per_day": 200,
                    "documents": 20,
                    "users": 3
                },
                "pricing": {
                    "weekly": 399,
                    "monthly": 1199,
                    "quarterly": 3199,
                    "yearly": 11499
                }
            },
            "premium": {
                "name": "Premium",
                "features": [
                    "🔹 5 Users",
                    "🔹 All Modules + Hearing Assessment",
                    "🔹 Custom Reports",
                    "🔹 Dedicated Helpdesk"
                ],
                "limits": {
                    "questions_per_day": 500,
                    "documents": 50,
                    "users": 5
                },
                "pricing": {
                    "weekly": 499,
                    "monthly": 1699,
                    "quarterly": 4599,
                    "yearly": 16499
                }
            },
            "enterprise": {
                "name": "Enterprise",
                "features": [
                    "🔹 10 Users",
                    "🔹 Full Suite + API Access",
                    "🔹 Unlimited Document Analysis",
                    "🔹 SLA Guarantee"
                ],
                "limits": {
                    "questions_per_day": -1,  # Unlimited
                    "documents": -1,  # Unlimited
                    "users": 10
                },
                "pricing": {
                    "weekly": 999,
                    "monthly": 3999,
                    "quarterly": 10999,
                    "yearly": 39999
                }
            }
        }
    
    def initialize_session_state(self):
        """Initialize subscription-related session state variables."""
        if 'subscription_plan' not in st.session_state:
            st.session_state.subscription_plan = 'free'
        
        if 'questions_asked_today' not in st.session_state:
            st.session_state.questions_asked_today = 0
        
        if 'last_question_date' not in st.session_state:
            st.session_state.last_question_date = datetime.date.today()
        
        if 'payment_completed' not in st.session_state:
            st.session_state.payment_completed = False
        
        # Reset daily counter if it's a new day
        if st.session_state.last_question_date != datetime.date.today():
            st.session_state.questions_asked_today = 0
            st.session_state.last_question_date = datetime.date.today()
    
    def can_ask_question(self) -> bool:
        """Check if user can ask a question based on their plan."""
        self.initialize_session_state()
        
        if st.session_state.subscription_plan == 'free':
            return st.session_state.questions_asked_today < 1
        
        if st.session_state.subscription_plan in self.plans:
            plan = self.plans[st.session_state.subscription_plan]
            daily_limit = plan['limits']['questions_per_day']
            
            if daily_limit == -1:  # Unlimited
                return True
            
            return st.session_state.questions_asked_today < daily_limit
        
        return False
    
    def increment_question_count(self):
        """Increment the question count for the day."""
        st.session_state.questions_asked_today += 1
    
    def get_remaining_questions(self) -> str:
        """Get remaining questions for the day."""
        if st.session_state.subscription_plan == 'free':
            remaining = 1 - st.session_state.questions_asked_today
            return f"{remaining} free question remaining"
        
        if st.session_state.subscription_plan in self.plans:
            plan = self.plans[st.session_state.subscription_plan]
            daily_limit = plan['limits']['questions_per_day']
            
            if daily_limit == -1:
                return "Unlimited questions"
            
            remaining = daily_limit - st.session_state.questions_asked_today
            return f"{remaining} questions remaining today"
        
        return "0 questions remaining"
    
    def show_upgrade_message(self):
        """Show upgrade message when limit is reached."""
        st.error("🚫 **Question Limit Reached!**")
        st.warning("You've used up your free question. Upgrade to continue asking questions!")
        
        if st.button("🚀 **Upgrade Now**", type="primary", use_container_width=True):
            st.session_state.show_subscription_page = True
            st.rerun()
    
    def show_subscription_plans(self):
        """Display subscription plans with beautiful card-based design."""
        st.markdown("## 🎯 **Choose Your Perfect Plan**")
        st.markdown("Select the ideal plan for your import-export documentation needs!")
        
        # Add custom CSS for beautiful plan cards
        # Enhanced CSS with inline styles for cards
        st.markdown("""
        <style>
        .plan-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 2px solid #e1e8ed;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
        }
        
        .plan-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .plan-card.popular {
            border-color: #4CAF50;
            position: relative;
        }
        
        .popular-badge {
            position: absolute;
            top: -10px;
            right: 20px;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .plan-header {
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .plan-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1976D2;
            margin-bottom: 0.5rem;
        }
        
        .plan-price {
            font-size: 2rem;
            font-weight: bold;
            color: #2E7D32;
            margin-bottom: 0.5rem;
        }
        
        .plan-period {
            color: #666;
            font-size: 0.9rem;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
            margin: 1rem 0;
        }
        
        .feature-item {
            padding: 0.3rem 0;
            color: #424242;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Billing period selection
        st.markdown("**💰 Choose Billing Period:**")
        billing_period = st.radio(
            "Select billing period:",
            ["Weekly", "Monthly", "Quarterly", "Yearly"],
            index=1,  # Default to Monthly
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Display all 6 plans in a 3x2 grid layout
        all_plans = ["explorer", "starter", "professional", "advanced", "premium", "enterprise"]
        
        # Top row - first 3 plans
        st.markdown("### 🚀 **Popular Plans**")
        cols_top = st.columns(3)
        for i, plan_key in enumerate(all_plans[:3]):
            plan = self.plans[plan_key]
            is_popular = plan_key == "professional"
            
            with cols_top[i]:
                self._render_single_plan_card(plan_key, plan, billing_period, is_popular)
        
        st.markdown("---")
        
        # Bottom row - last 3 plans  
        st.markdown("### 💼 **Advanced Plans**")
        cols_bottom = st.columns(3)
        for i, plan_key in enumerate(all_plans[3:]):
            plan = self.plans[plan_key]
            is_popular = plan_key == "premium"  # Make premium popular in bottom row
            
            with cols_bottom[i]:
                self._render_single_plan_card(plan_key, plan, billing_period, is_popular)
    
    def _render_single_plan_card(self, plan_key: str, plan: dict, billing_period: str, is_popular: bool = False):
        """Render a single plan card using Streamlit components."""
        # Get prices from plan data
        if billing_period == "Weekly":
            display_price = plan['pricing']['weekly']
            period_text = "/week"
        elif billing_period == "Monthly":
            display_price = plan['pricing']['monthly']
            period_text = "/month"
        elif billing_period == "Quarterly":
            display_price = plan['pricing']['quarterly']
            period_text = "/quarter"
        else:  # Yearly
            display_price = plan['pricing']['yearly']
            period_text = "/year"
        
        # Format price - handle both numbers and strings
        if isinstance(display_price, (int, float)):
            formatted_price = f"₹{int(display_price):,}"
        else:
            formatted_price = str(display_price)  # For "Custom" etc.
        
        # Plan colors
        plan_colors = {
            "explorer": "#28a745",
            "starter": "#007bff", 
            "professional": "#f72585",
            "advanced": "#6f42c1",
            "premium": "#fd7e14",
            "enterprise": "#20c997"
        }
        plan_color = plan_colors.get(plan_key, "#667eea")
        
        # Build features list
        questions_text = "Unlimited" if plan['limits']['questions_per_day'] == -1 else f"{plan['limits']['questions_per_day']}"
        docs_text = "Unlimited" if plan['limits']['documents'] == -1 else f"{plan['limits']['documents']}"
        
        features = [
            f"📊 {questions_text} questions per day",
            f"💾 {docs_text} document limit", 
            f"👥 {plan['limits']['users']} user(s)",
            "⚡ Fast response time"
        ]
        
        if plan_key in ['professional', 'advanced', 'premium', 'enterprise']:
            features.append("🎯 Priority support")
        
        if plan_key in ['advanced', 'premium', 'enterprise']:
            features.append("📈 Analytics dashboard")
            
        if plan_key in ['premium', 'enterprise']:
            features.append("🔧 Custom reports")
            
        if plan_key == 'enterprise':
            features.append("🔑 API access")
        
        # Use a simple container with native Streamlit components
        with st.container():
            # Create card using CSS
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {plan_color}15, {plan_color}25);
                border: 2px solid {plan_color};
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                position: relative;
            ">
            </div>
            """, unsafe_allow_html=True)
            
            # Popular badge
            if is_popular:
                st.markdown(f"<div style='text-align: center; color: {plan_color}; font-weight: bold; margin-bottom: 10px;'>� POPULAR</div>", unsafe_allow_html=True)
            
            # Plan title and price
            st.markdown(f"### �🚀 {plan['name']}")
            st.markdown(f"#### {formatted_price} {period_text}")
            
            # Features
            st.markdown("**🌟 Features:**")
            for feature in features:
                st.markdown(f"• {feature}")
            
            # Select button
            button_type = "primary" if is_popular else "secondary"
            if st.button(f"🚀 Choose {plan['name']}", key=f"select_{plan_key}_{billing_period}", 
                        type=button_type, use_container_width=True):
                st.session_state.selected_plan = plan_key
                st.session_state.selected_period = billing_period
                # Store numeric amount for payment processing, or 0 for custom
                st.session_state.selected_amount = display_price if isinstance(display_price, (int, float)) else 0
                st.session_state.show_payment_page = True
                st.rerun()
    
    def show_payment_page(self):
        """Show enhanced payment processing page."""
        if not hasattr(st.session_state, 'selected_plan'):
            st.error("No plan selected. Please go back and select a plan.")
            return
            
        # Check and set default values for missing session state variables
        if not hasattr(st.session_state, 'selected_period'):
            st.session_state.selected_period = "Monthly"
            
        if not hasattr(st.session_state, 'selected_amount'):
            # Calculate default amount based on selected plan and period
            plan = self.plans[st.session_state.selected_plan]
            if st.session_state.selected_period.lower() in plan['pricing']:
                st.session_state.selected_amount = plan['pricing'][st.session_state.selected_period.lower()]
            else:
                st.session_state.selected_amount = plan['pricing']['monthly']
        
        plan_name = self.plans[st.session_state.selected_plan]['name']
        period = st.session_state.selected_period
        amount = st.session_state.selected_amount
        
        # Payment page styling
        st.markdown("""
        <style>
        .payment-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .payment-summary {
            background: white;
            color: #2c3e50;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .payment-method {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 2px solid #e1e8ed;
            transition: all 0.3s ease;
        }
        
        .payment-method:hover {
            border-color: #667eea;
            background: #f0f4ff;
        }
        
        .secure-badge {
            background: #28a745;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            display: inline-block;
            margin: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Payment header
        st.markdown(f"""
        <div class="payment-container">
            <h2>💳 Complete Your Purchase</h2>
            <p>You're just one step away from unlocking premium features!</p>
            <div class="secure-badge">🔒 Secure Payment</div>
            <div class="secure-badge">💯 Money Back Guarantee</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Order summary
        st.markdown(f"""
        <div class="payment-summary">
            <h3>📋 Order Summary</h3>
            <table style="width: 100%; margin-top: 1rem;">
                <tr>
                    <td><strong>Plan:</strong></td>
                    <td>{plan_name}</td>
                </tr>
                <tr>
                    <td><strong>Billing Period:</strong></td>
                    <td>{period.title()}</td>
                </tr>
                <tr>
                    <td><strong>Amount:</strong></td>
                    <td style="font-size: 1.5rem; color: #667eea;"><strong>₹{amount:,}</strong></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        # Payment methods
        st.markdown("### 💳 **Choose Your Payment Method**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="payment-method">
                <h4>🇮🇳 Razorpay</h4>
                <p>• UPI, Cards, NetBanking<br>
                • Instant payment confirmation<br>
                • Trusted by millions in India</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💳 **Pay with Razorpay**", use_container_width=True, type="primary"):
                self.process_razorpay_payment(amount)
        
        with col2:
            st.markdown("""
            <div class="payment-method">
                <h4>🌐 Stripe</h4>
                <p>• International cards accepted<br>
                • Advanced fraud protection<br>
                • Global payment processing</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🌐 **Pay with Stripe**", use_container_width=True, type="secondary"):
                self.process_stripe_payment(amount)
        
        # Security information
        st.markdown("""
        ---
        ### 🔒 **Security & Trust**
        
        ✅ **SSL Encrypted** - Your payment information is protected  
        ✅ **PCI Compliant** - Industry standard security  
        ✅ **No Hidden Fees** - What you see is what you pay  
        ✅ **Instant Access** - Unlock features immediately after payment  
        ✅ **24/7 Support** - We're here to help if you need assistance  
        """)
        
        # Demo payment (for testing)
        with st.expander("🧪 **Demo Mode** (For Testing)", expanded=False):
            st.markdown("**Test the payment flow without real money**")
            if st.button("✅ **Simulate Successful Payment**", type="secondary", use_container_width=True):
                self.complete_payment_success()
            
            st.markdown("**Test Card Numbers:**")
            st.code("Razorpay: 4111 1111 1111 1111")
            st.code("Stripe: 4242 4242 4242 4242")
        
        # Back button
        if st.button("⬅️ **Back to Plans**", type="secondary"):
            if hasattr(st.session_state, 'show_payment_page'):
                del st.session_state.show_payment_page
            st.rerun()
    
    def process_razorpay_payment(self, amount: int):
        """Process payment via Razorpay with enhanced UI."""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff9a56 0%, #ff6b6b 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
            <h3>🔄 Redirecting to Razorpay...</h3>
            <p>You will be redirected to secure Razorpay payment gateway</p>
        </div>
        """, unsafe_allow_html=True)
        
        # In a real implementation, you would:
        # 1. Create Razorpay order
        # 2. Redirect to Razorpay payment page
        # 3. Handle webhook for payment confirmation
        
        # For demo purposes, show a styled form
        st.markdown("### 💳 **Razorpay Payment Details**")
        
        with st.form("razorpay_payment"):
            col1, col2 = st.columns(2)
            
            with col1:
                email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
                phone = st.text_input("📱 Phone Number", placeholder="+91 9876543210")
            
            with col2:
                name = st.text_input("👤 Full Name", placeholder="Your Full Name")
                address = st.text_area("🏠 Address", placeholder="Your billing address")
            
            st.markdown("---")
            st.markdown("**🔒 Payment Methods Available:**")
            st.markdown("• 💳 Credit/Debit Cards • 📱 UPI • 🏦 Net Banking • 💰 Wallets")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                terms_agreed = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            with col2:
                submitted = st.form_submit_button("🚀 **Pay Now**", type="primary", use_container_width=True)
            
            if submitted:
                if email and phone and name and terms_agreed:
                    # Simulate payment processing
                    with st.spinner("🔄 Processing your payment securely..."):
                        import time
                        time.sleep(3)
                    self.complete_payment_success()
                else:
                    st.error("❌ Please fill all required fields and agree to terms")
    
    def process_stripe_payment(self, amount: int):
        """Process payment via Stripe with enhanced UI."""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
            <h3>🔄 Redirecting to Stripe...</h3>
            <p>You will be redirected to secure Stripe payment gateway</p>
        </div>
        """, unsafe_allow_html=True)
        
        # In a real implementation, you would:
        # 1. Create Stripe checkout session
        # 2. Redirect to Stripe payment page
        # 3. Handle webhook for payment confirmation
        
        # For demo purposes, show a styled form
        st.markdown("### 💳 **Stripe Payment Details**")
        
        with st.form("stripe_payment"):
            # Customer details
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
                name = st.text_input("👤 Cardholder Name", placeholder="Name on Card")
            
            with col2:
                country = st.selectbox("🌍 Country", ["India", "United States", "United Kingdom", "Canada", "Australia", "Other"])
                postal_code = st.text_input("📮 Postal Code", placeholder="110001")
            
            # Card details
            st.markdown("**💳 Card Information**")
            card_number = st.text_input("Card Number", placeholder="4242 4242 4242 4242", help="Use 4242 4242 4242 4242 for testing")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                expiry_month = st.selectbox("Month", [f"{i:02d}" for i in range(1, 13)])
            with col2:
                expiry_year = st.selectbox("Year", [str(2024 + i) for i in range(10)])
            with col3:
                cvv = st.text_input("CVV", placeholder="123", max_chars=4)
            
            st.markdown("---")
            st.markdown("**🔒 Stripe Security Features:**")
            st.markdown("• 🛡️ Advanced Fraud Detection • 🔐 3D Secure Authentication • 💯 PCI DSS Compliant")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                terms_agreed = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            with col2:
                submitted = st.form_submit_button("🚀 **Pay Now**", type="primary", use_container_width=True)
            
            if submitted:
                if card_number and expiry_month and expiry_year and cvv and email and name and terms_agreed:
                    # Simulate payment processing
                    with st.spinner("🔄 Processing your payment securely..."):
                        import time
                        time.sleep(3)
                    self.complete_payment_success()
                else:
                    st.error("❌ Please fill all required fields and agree to terms")
    
    def complete_payment_success(self):
        """Handle successful payment completion with celebration UI."""
        st.session_state.subscription_plan = st.session_state.selected_plan
        st.session_state.payment_completed = True
        st.session_state.questions_asked_today = 0  # Reset question count
        st.session_state.subscription_start_date = datetime.date.today()
        
        # Clear payment session state
        if hasattr(st.session_state, 'show_payment_page'):
            del st.session_state.show_payment_page
        if hasattr(st.session_state, 'show_subscription_page'):
            del st.session_state.show_subscription_page
        
        # Beautiful success animation
        plan_name = self.plans[st.session_state.selected_plan]['name']
        plan_details = self.plans[st.session_state.selected_plan]
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            border: 2px solid #4CAF50;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3);
            animation: pulse 2s infinite;
        ">
            <div style="font-size: 4rem; color: #4CAF50; margin-bottom: 1rem;">
                🎉
            </div>
            <h2 style="color: #2E7D32; margin-bottom: 1rem;">
                🎊 Payment Successful! 🎊
            </h2>
            <p style="font-size: 1.2rem; color: #388E3C; margin-bottom: 1.5rem;">
                Welcome to your new subscription plan!
            </p>
        </div>
        
        <style>
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.balloons()
        
        # Plan details in a beautiful card
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-left: 5px solid #4CAF50;
        ">
            <h3 style="color: #1976D2; margin-bottom: 1.5rem;">🚀 Your {plan_name} Plan is Active!</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                    <div style="font-size: 2rem; color: #FF9800; margin-bottom: 0.5rem;">📊</div>
                    <div style="font-weight: bold; color: #424242;">{plan_details['limits']['questions_per_day']} Questions</div>
                    <div style="color: #666;">Per Day</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                    <div style="font-size: 2rem; color: #9C27B0; margin-bottom: 0.5rem;">💾</div>
                    <div style="font-weight: bold; color: #424242;">{plan_details['limits']['documents']} Documents</div>
                    <div style="color: #666;">Upload Limit</div>
                </div>
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                    <div style="font-size: 2rem; color: #4CAF50; margin-bottom: 0.5rem;">⚡</div>
                    <div style="font-weight: bold; color: #424242;">Fast Response</div>
                    <div style="color: #666;">Priority Queue</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 **Start Asking Questions!**", type="primary", use_container_width=True):
                st.rerun()
            
            if st.button("📧 **Send Receipt to Email**", use_container_width=True):
                st.success("📧 Receipt sent to your email address!")
        
        # Additional benefits showcase
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        ">
            <h4>🎁 Features You've Unlocked:</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
                <div>✨ Priority support response</div>
                <div>🔄 Conversation history saved</div>
                <div>📱 Mobile-optimized experience</div>
                <div>🔔 Usage alerts and notifications</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto refresh after 3 seconds
        import time
        time.sleep(2)
        st.rerun()
    
    def get_current_plan_info(self) -> Dict:
        """Get current plan information."""
        if st.session_state.subscription_plan == 'free':
            return {
                "name": "Free Plan",
                "features": ["🔹 1 Free Question"],
                "limits": {"questions_per_day": 1}
            }
        
        return self.plans.get(st.session_state.subscription_plan, {})
    
    def show_current_plan_status(self):
        """Show current plan status in sidebar."""
        plan_info = self.get_current_plan_info()
        
        st.markdown("### 🎯 **Current Plan**")
        st.markdown(f"**{plan_info['name']}**")
        
        if st.session_state.subscription_plan != 'free':
            st.markdown("**Features:**")
            for feature in plan_info['features']:
                st.markdown(f"- {feature}")
        
        # Show usage stats
        remaining = self.get_remaining_questions()
        st.markdown(f"**Usage:** {remaining}")
        
        # Upgrade button for free users
        if st.session_state.subscription_plan == 'free':
            if st.button("🚀 **Upgrade Plan**", use_container_width=True):
                st.session_state.show_subscription_page = True
                st.rerun()
