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
                    "1 User",
                    "All Basic Modules",
                    "Basic Reports"
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
                    "2 Users",
                    "Advanced Modules",
                    "Priority Support"
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
                    "3 Users",
                    "All Modules",
                    "Monthly Compliance Reports",
                    "Priority Support"
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
                    "5 Users",
                    "All Modules + Hearing Assessment",
                    "Custom Reports",
                    "Dedicated Helpdesk"
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
                    "10 Users",
                    "Full Suite + API Access",
                    "Unlimited Document Analysis",
                    "SLA Guarantee"
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
        """Initialize session state variables."""
        if 'user_subscription' not in st.session_state:
            st.session_state.user_subscription = 'free'
        if 'questions_asked' not in st.session_state:
            st.session_state.questions_asked = 0
    
    def show_current_plan_status(self):
        """Display current subscription plan status in sidebar."""
        current_plan = st.session_state.get('user_subscription', 'free')
        
        if current_plan == 'free':
            st.markdown("### 📊 **Current Plan**")
            st.info("**Free Plan** 🆓")
            questions_asked = st.session_state.get('questions_asked', 0)
            remaining = max(0, 1 - questions_asked)
            st.markdown(f"**Questions:** {remaining}/1 remaining")
            
            if remaining == 0:
                st.warning("⚠️ Limit reached!")
                if st.button("🚀 **Upgrade Now**", type="primary", use_container_width=True):
                    st.session_state.show_subscription_page = True
                    st.rerun()
        else:
            # Paid plan
            plan_info = self.plans.get(current_plan, {})
            plan_name = plan_info.get('name', current_plan.title())
            
            st.markdown("### 📊 **Current Plan**")
            st.success(f"**{plan_name}** ✅")
            
            # Show usage stats
            remaining_text = self.get_remaining_questions()
            st.markdown(f"**Usage:** {remaining_text}")
            
            # Show plan features
            daily_limit = plan_info.get('limits', {}).get('questions_per_day', 0)
            docs_limit = plan_info.get('limits', {}).get('documents', 0)
            users_limit = plan_info.get('limits', {}).get('users', 1)
            
            st.markdown("**Plan Features:**")
            if daily_limit == -1:
                st.markdown("• ♾️ Unlimited questions")
            else:
                st.markdown(f"• 📊 {daily_limit} questions/day")
            
            if docs_limit == -1:
                st.markdown("• 📄 Unlimited documents")
            else:
                st.markdown(f"• 📄 {docs_limit} documents")
                
            st.markdown(f"• 👥 {users_limit} user(s)")
            
            if st.button("🔄 **Change Plan**", use_container_width=True):
                st.session_state.show_subscription_page = True
                st.rerun()
    
    def can_ask_question(self, user_id: str = "default") -> bool:
        """Check if user can ask a question based on their subscription."""
        # Get current user subscription
        current_plan = st.session_state.get('user_subscription', 'free')
        
        # Free users get 1 question total
        if current_plan == 'free':
            questions_asked = st.session_state.get('questions_asked', 0)
            return questions_asked < 1
        
        # Paid users based on daily limits
        if current_plan in self.plans:
            daily_limit = self.plans[current_plan]['limits']['questions_per_day']
            if daily_limit == -1:  # Unlimited
                return True
            
            today = datetime.date.today().isoformat()
            daily_count = st.session_state.get(f'questions_today_{today}', 0)
            return daily_count < daily_limit
        
        return False
    
    def increment_question_count(self, user_id: str = "default"):
        """Increment the question count for tracking."""
        current_plan = st.session_state.get('user_subscription', 'free')
        
        if current_plan == 'free':
            # Track total questions for free users
            if 'questions_asked' not in st.session_state:
                st.session_state.questions_asked = 0
            st.session_state.questions_asked += 1
        else:
            # Track daily questions for paid users
            today = datetime.date.today().isoformat()
            daily_key = f'questions_today_{today}'
            if daily_key not in st.session_state:
                st.session_state[daily_key] = 0
            st.session_state[daily_key] += 1
    
    def get_remaining_questions(self, user_id: str = "default") -> str:
        """Get remaining questions for the user."""
        current_plan = st.session_state.get('user_subscription', 'free')
        
        if current_plan == 'free':
            questions_asked = st.session_state.get('questions_asked', 0)
            remaining = max(0, 1 - questions_asked)
            return f"{remaining} question(s) remaining (Free plan)"
        
        if current_plan in self.plans:
            daily_limit = self.plans[current_plan]['limits']['questions_per_day']
            if daily_limit == -1:
                return "Unlimited questions (Premium plan)"
            
            today = datetime.date.today().isoformat()
            daily_count = st.session_state.get(f'questions_today_{today}', 0)
            remaining = max(0, daily_limit - daily_count)
            return f"{remaining}/{daily_limit} questions remaining today"
        
        return "Unknown plan"
    
    def show_upgrade_prompt(self):
        """Show upgrade prompt when user hits limits."""
        st.warning("⚠️ **Question limit reached!**")
        st.info("📈 **Upgrade to continue asking questions with advanced features:**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 **View Subscription Plans**", type="primary", use_container_width=True):
                st.session_state.show_subscription_page = True
                st.rerun()
        
        with col2:
            if st.button("💰 **Quick Upgrade**", type="secondary", use_container_width=True):
                st.session_state.show_subscription_page = True
                st.rerun()
    
    def show_upgrade_message(self):
        """Show upgrade message when user hits limits. Alias for show_upgrade_prompt."""
        self.show_upgrade_prompt()
    
    def show_subscription_plans(self):
        """Display subscription plans in a 3x2 grid layout."""
        st.title("💳 **Choose Your Subscription Plan**")
        st.markdown("**Unlock unlimited access to our AI-powered document analysis system!**")
        
        # Add custom CSS for better styling
        st.markdown("""
        <style>
        .plan-card {
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: #f9f9f9;
        }
        
        .plan-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1f4e79;
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
        """Render a single plan card using reliable Streamlit components."""
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
        
        # Use Streamlit's native components for reliable rendering
        # Simple card layout using expander
        with st.expander(f"🚀 {plan['name']} - {formatted_price} {period_text}", expanded=True):
            if is_popular:
                st.success("🔥 POPULAR CHOICE!")
            
            st.markdown("**🌟 Features:**")
            for feature in features:
                st.markdown(f"• {feature}")
            
            # Select button
            button_type = "primary" if is_popular else "secondary"
            if st.button(f"Choose {plan['name']}", key=f"select_{plan_key}_{billing_period}", 
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
            plan_key = st.session_state.selected_plan
            period = st.session_state.selected_period.lower()
            if plan_key in self.plans and period in self.plans[plan_key]['pricing']:
                st.session_state.selected_amount = self.plans[plan_key]['pricing'][period]
            else:
                st.session_state.selected_amount = 0
        
        plan_key = st.session_state.selected_plan
        period = st.session_state.selected_period
        amount = st.session_state.selected_amount
        
        plan = self.plans.get(plan_key, {})
        plan_name = plan.get('name', plan_key)
        
        st.title("💳 **Payment & Checkout**")
        st.markdown("---")
        
        # Order Summary
        st.subheader("📋 **Order Summary**")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Plan:** {plan_name}")
            st.markdown(f"**Billing Period:** {period}")
            st.markdown(f"**Amount:** ₹{amount:,}")
        
        with col2:
            if st.button("← **Change Plan**", type="secondary"):
                del st.session_state.show_payment_page
                st.rerun()
        
        st.markdown("---")
        
        # Payment Method Selection
        st.subheader("💰 **Select Payment Method**")
        
        payment_method = st.radio(
            "Choose your preferred payment method:",
            ["💳 Credit/Debit Card", "🏦 Net Banking", "📱 UPI", "💰 Wallet"],
            horizontal=True
        )
        
        # Payment Forms (Demo)
        st.markdown("---")
        st.subheader("🔐 **Payment Details**")
        
        if "💳" in payment_method:  # Credit/Debit Card
            col1, col2 = st.columns(2)
            with col1:
                card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
                cardholder_name = st.text_input("Cardholder Name", placeholder="John Doe")
            with col2:
                expiry = st.text_input("Expiry Date", placeholder="MM/YY")
                cvv = st.text_input("CVV", placeholder="123", type="password")
                
        elif "🏦" in payment_method:  # Net Banking
            bank = st.selectbox("Select Your Bank", [
                "State Bank of India", "HDFC Bank", "ICICI Bank", 
                "Axis Bank", "Kotak Mahindra Bank", "Other"
            ])
            
        elif "📱" in payment_method:  # UPI
            upi_id = st.text_input("UPI ID", placeholder="yourname@upi")
            
        elif "💰" in payment_method:  # Wallet
            wallet = st.selectbox("Select Wallet", [
                "Paytm", "PhonePe", "Google Pay", "Amazon Pay", "Other"
            ])
        
        # Billing Address
        st.markdown("---")
        st.subheader("📍 **Billing Address**")
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="john@example.com")
            phone = st.text_input("Phone", placeholder="+91 9876543210")
            
        with col2:
            address = st.text_area("Address", placeholder="Street, City, State")
            pincode = st.text_input("PIN Code", placeholder="123456")
            
        # Payment Processing
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"💳 **Pay ₹{amount:,}**", type="primary", use_container_width=True):
                # Simulate payment processing
                with st.spinner("Processing payment..."):
                    import time
                    time.sleep(2)  # Simulate processing time
                
                # Payment successful
                st.success("✅ **Payment Successful!**")
                st.balloons()
                
                # Update user subscription
                st.session_state.user_subscription = plan_key
                st.session_state.subscription_start = datetime.datetime.now()
                
                # Clear payment session
                if hasattr(st.session_state, 'show_payment_page'):
                    del st.session_state.show_payment_page
                if hasattr(st.session_state, 'show_subscription_page'):
                    del st.session_state.show_subscription_page
                
                st.markdown("---")
                st.markdown("### 🎉 **Welcome to your new plan!**")
                st.markdown(f"You now have access to **{plan_name}** features.")
                
                if st.button("🏠 **Go to Dashboard**", type="primary"):
                    st.rerun()
        
        # Security Note
        st.markdown("---")
        st.info("🔒 **Your payment information is secure and encrypted. We use industry-standard security measures to protect your data.**")
        
        # Support
        st.markdown("---")
        st.markdown("### 📞 **Need Help?**")
        st.markdown("Contact our support team: **support@yourcompany.com** | **+91-XXXXXXXXXX**")
