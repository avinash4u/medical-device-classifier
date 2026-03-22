# 🔐 LLM API Key Configuration Guide

## Current Implementation

The medical device classifier uses **Google Gemini API** for LLM extraction. Here's how the API key is configured:

### **📍 Where API Key is Used:**

1. **extraction_engine.py** (Lines 238, 471, 586):
   ```python
   api_key = os.getenv('GEMINI_API_KEY')
   ```

2. **Multiple Methods**:
   - `_llm_extract_all_fields()` - Comprehensive extraction
   - `_llm_extract_device_name()` - Device name extraction  
   - `_llm_extract_field()` - General field extraction

### **🔧 How to Set Up API Key:**

#### **Option 1: Environment Variable (Recommended)**
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

#### **Option 2: .env File (Development)**
Create `.env` file in project root:
```env
GEMINI_API_KEY=your-gemini-api-key-here
```

Add to `.gitignore`:
```gitignore
.env
```

#### **Option 3: System Environment**
```bash
# For current session
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc

# For permanent
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bash_profile
```

### **🔑 Getting Your Gemini API Key:**

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Set it using one of the methods above

### **🛡️ Security Notes:**

- ✅ **Never commit API keys** to Git
- ✅ **Use environment variables** in production
- ✅ **Keep keys private** and secure
- ✅ **Rotate keys regularly** for security

### **🔄 How It Works:**

1. **Training Data First**: System tries to match with training examples
2. **LLM Fallback**: If no training match, uses Gemini API
3. **Pattern Matching**: Final fallback if API unavailable
4. **Graceful Degradation**: Always works even without API key

### **📊 Current Status:**
- 🔍 **API Key Source**: Environment variable (`GEMINI_API_KEY`)
- 🌐 **API Provider**: Google Gemini (gemini-1.5-flash)
- 🔄 **Fallback Strategy**: Three-tier extraction system
- ✅ **No API Key Required**: System works without LLM
