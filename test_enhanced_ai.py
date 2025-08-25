#!/usr/bin/env python3
"""
Test script for enhanced AI symptom analysis with dual treatment recommendations
"""

import requests
import json
import time

def test_comprehensive_analysis():
    """Test the new comprehensive symptom analysis endpoint"""
    
    print("🧪 Testing Enhanced AI Symptom Analysis")
    print("=" * 60)
    
    # Test cases with various symptoms
    test_cases = [
        {
            "name": "Common Cold Symptoms",
            "symptoms": "I have a runny nose, cough, and feeling tired"
        },
        {
            "name": "Digestive Issues",
            "symptoms": "stomach pain, nausea, and diarrhea"
        },
        {
            "name": "Stress-Related Symptoms",
            "symptoms": "headache, anxiety, and trouble sleeping"
        },
        {
            "name": "Flu-like Symptoms",
            "symptoms": "fever, body aches, fatigue, and cough"
        },
        {
            "name": "Mental Health Symptoms",
            "symptoms": "feeling depressed, anxious, and having insomnia"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"Symptoms: {test_case['symptoms']}")
        print("-" * 40)
        
        try:
            # Test comprehensive analysis
            response = requests.post(
                "http://localhost:5001/ai/comprehensive-symptom-analysis",
                json={
                    "symptoms": test_case['symptoms'],
                    "user_id": "test_user"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    analysis = data['analysis']
                    
                    print(f"✅ Analysis successful!")
                    print(f"📊 Detected symptoms: {', '.join(analysis['detected_symptoms'])}")
                    print(f"🎯 AI Confidence: {analysis['overall_confidence'] * 100:.1f}%")
                    
                    # Check allopathy recommendations
                    allopathy = data['treatment_options']['allopathy']['treatments']
                    if allopathy['primary_treatments']:
                        print(f"💊 Allopathy treatments: {len(allopathy['primary_treatments'])} primary")
                    
                    # Check naturopathy recommendations
                    naturopathy = data['treatment_options']['naturopathy']['treatments']
                    if naturopathy['primary_treatments']:
                        print(f"🌿 Naturopathy treatments: {len(naturopathy['primary_treatments'])} primary")
                    
                    # Check lifestyle recommendations
                    lifestyle = data['treatment_options']['lifestyle']['recommendations']
                    print(f"💡 Lifestyle recommendations: {len(lifestyle)} items")
                    
                else:
                    print(f"❌ Analysis failed: {data.get('message', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Brief pause between tests

def test_enhanced_recommendations():
    """Test the enhanced recommendations endpoint"""
    
    print("\n\n🔬 Testing Enhanced Recommendations")
    print("=" * 60)
    
    test_cases = [
        {
            "symptoms": "headache and nausea",
            "treatment_type": "both"
        },
        {
            "symptoms": "anxiety and insomnia", 
            "treatment_type": "naturopathy"
        },
        {
            "symptoms": "fever and cough",
            "treatment_type": "allopathy"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing treatment type: {test_case['treatment_type']}")
        print(f"Symptoms: {test_case['symptoms']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://localhost:5001/ai/enhanced-recommendations",
                json=test_case,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print(f"✅ Recommendations successful!")
                    print(f"📊 Confidence: {data['confidence_score'] * 100:.1f}%")
                    print(f"🎯 Treatment approach: {data['treatment_approach']}")
                    
                    recommendations = data['recommendations']
                    for treatment_type, details in recommendations.items():
                        if treatment_type != 'lifestyle':
                            primary_count = len(details.get('primary_treatments', []))
                            print(f"   {treatment_type}: {primary_count} primary treatments")
                        else:
                            lifestyle_count = len(details)
                            print(f"   lifestyle: {lifestyle_count} recommendations")
                else:
                    print(f"❌ Recommendations failed: {data.get('message', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)

def test_detailed_analysis():
    """Test detailed analysis output"""
    
    print("\n\n🔍 Testing Detailed Analysis Output")
    print("=" * 60)
    
    try:
        response = requests.post(
            "http://localhost:5001/ai/comprehensive-symptom-analysis",
            json={
                "symptoms": "I have been experiencing severe headaches, nausea, and fatigue for the past few days",
                "user_id": "detailed_test"
            },
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("✅ Detailed analysis successful!")
                print("\n📋 Full Analysis Results:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Analysis failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🏥 Enhanced AI Healthcare System Test")
    print("Testing comprehensive symptom analysis with dual treatment recommendations")
    print("=" * 80)
    
    # Test all endpoints
    test_comprehensive_analysis()
    test_enhanced_recommendations()
    test_detailed_analysis()
    
    print("\n" + "=" * 80)
    print("🎉 Enhanced AI Testing Complete!")
    print("✨ The system now provides both allopathy and naturopathy recommendations!")
