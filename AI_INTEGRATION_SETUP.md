# 🤖 AI Integration Setup Guide

## OpenAI GPT Integration for Enhanced Medical Analysis

This guide will help you set up OpenAI GPT integration for advanced medical symptom analysis and recommendations.

### 🔑 Step 1: Get OpenAI API Key

1. **Visit OpenAI Platform**: Go to [https://platform.openai.com](https://platform.openai.com)
2. **Create Account**: Sign up or log in to your OpenAI account
3. **Navigate to API Keys**: Go to "API Keys" section in your dashboard
4. **Create New Key**: Click "Create new secret key"
5. **Copy the Key**: Save your API key securely (it starts with `sk-`)

### ⚙️ Step 2: Configure Environment Variables

1. **Navigate to AI Service Directory**:
   ```bash
   cd ai_service
   ```

2. **Create Environment File**:
   ```bash
   cp .env.example .env
   ```

3. **Edit the .env file** and add your OpenAI API key:
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=sk-your-actual-api-key-here
   
   # AI Service Configuration
   AI_MODEL=gpt-3.5-turbo
   AI_MAX_TOKENS=1000
   AI_TEMPERATURE=0.3
   
   # Medical AI Settings
   MEDICAL_DISCLAIMER=true
   EMERGENCY_KEYWORDS=chest pain,difficulty breathing,severe bleeding,unconscious,stroke symptoms
   
   # Rate Limiting
   MAX_REQUESTS_PER_MINUTE=60
   MAX_REQUESTS_PER_HOUR=1000
   ```

### 📦 Step 3: Install Required Dependencies

1. **Install Python Dependencies**:
   ```bash
   cd ai_service
   pip install -r requirements.txt
   ```

   This will install:
   - `openai==1.3.0` - OpenAI Python client
   - `python-dotenv==1.0.0` - Environment variable management

### 🚀 Step 4: Test the Integration

1. **Start the AI Service**:
   ```bash
   cd ai_service
   python app.py
   ```

2. **Check AI Status**:
   Visit: http://localhost:5001/ai/status
   
   You should see:
   ```json
   {
     "ai_enhanced": true,
     "gpt_available": true,
     "model": "gpt-3.5-turbo",
     "capabilities": [
       "Basic symptom analysis",
       "Medicine database search", 
       "Health recommendations",
       "GPT-powered analysis",
       "Advanced medicine recommendations",
       "Personalized insights"
     ]
   }
   ```

### 🏥 Step 5: Use GPT-Enhanced Features

#### **New Endpoints Available:**

1. **GPT Symptom Analysis**:
   ```
   POST http://localhost:5001/ai/gpt-analyze
   ```
   
2. **GPT Medicine Recommendations**:
   ```
   POST http://localhost:5001/ai/gpt-medicine-recommendations
   ```
   
3. **Personalized Health Insights**:
   ```
   POST http://localhost:5001/ai/health-insights
   ```

#### **Frontend Integration:**

- **Enhanced Symptoms Page**: Now includes GPT-powered analysis option
- **Analyzer Selection**: Choose between Enhanced AI or GPT-powered analysis
- **Advanced Analysis**: More detailed, conversational medical insights

### 💰 Cost Considerations

#### **OpenAI Pricing (as of 2024)**:
- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Typical Analysis**: 500-1000 tokens per request
- **Estimated Cost**: $0.001-$0.002 per analysis

#### **Cost Optimization**:
- Set reasonable token limits (`AI_MAX_TOKENS=1000`)
- Use lower temperature for medical analysis (`AI_TEMPERATURE=0.3`)
- Implement rate limiting to prevent abuse

### 🔒 Security Best Practices

1. **API Key Security**:
   - Never commit `.env` file to version control
   - Use environment variables in production
   - Rotate API keys regularly

2. **Rate Limiting**:
   - Implement request limits per user
   - Monitor API usage
   - Set up alerts for unusual activity

3. **Medical Compliance**:
   - Always include medical disclaimers
   - Emphasize professional consultation
   - Log all medical analyses for audit

### 🛠️ Troubleshooting

#### **Common Issues:**

1. **"Enhanced AI service not available"**:
   - Check if OpenAI API key is set correctly
   - Verify internet connection
   - Check API key permissions

2. **"Rate limit exceeded"**:
   - Wait before making more requests
   - Check your OpenAI usage limits
   - Implement request queuing

3. **"Invalid API key"**:
   - Verify the API key format (starts with `sk-`)
   - Check if key is active in OpenAI dashboard
   - Regenerate key if necessary

#### **Debug Mode:**

Enable debug logging by setting:
```env
DEBUG=true
```

### 🔄 Alternative AI Services

If you prefer other AI services, you can also configure:

```env
# Alternative AI Services (Optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
```

### 📊 Monitoring and Analytics

1. **Usage Tracking**: Monitor API calls and costs
2. **Performance Metrics**: Track response times and accuracy
3. **User Feedback**: Collect feedback on AI analysis quality

### 🎯 Benefits of GPT Integration

✅ **More Detailed Analysis**: Comprehensive, conversational medical insights
✅ **Better Context Understanding**: Considers patient history and demographics  
✅ **Natural Language**: Easy-to-understand explanations
✅ **Emergency Detection**: Advanced pattern recognition for urgent symptoms
✅ **Personalized Recommendations**: Tailored advice based on user context
✅ **Continuous Learning**: Benefits from OpenAI's ongoing model improvements

### 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review OpenAI documentation: https://platform.openai.com/docs
3. Check application logs for detailed error messages

---

**⚠️ Important Medical Disclaimer**: This AI integration is for informational purposes only and should not replace professional medical advice. Always consult qualified healthcare professionals for medical diagnosis and treatment.
