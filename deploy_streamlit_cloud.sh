#!/bin/bash
# 🚀 Streamlit Cloud Deployment Script

echo "🌟 Deploying Medical Device Classifier to Streamlit Cloud"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit not found. Installing..."
    pip install streamlit
fi

# Login to Streamlit Cloud
echo "🔐 Please login to Streamlit Cloud:"
echo "   streamlit login"
echo ""
echo "After login, press Enter to continue..."
read

# Deploy to Streamlit Cloud
echo "📤 Deploying to Streamlit Cloud..."
streamlit deploy

echo ""
echo "✅ Deployment complete!"
echo "📍 Your app will be available at: https://medical-device-classifier.streamlit.app"
echo ""
echo "📋 Next steps:"
echo "   1. Configure custom domain (optional)"
echo "   2. Set up environment variables for LLM API keys"
echo "   3. Monitor app usage and performance"
