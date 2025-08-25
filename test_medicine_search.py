#!/usr/bin/env python3
"""
Test script for the AI medicine search endpoint
"""

import requests
import json

def test_medicine_search():
    """Test the medicine search endpoint"""
    url = "http://localhost:5001/ai/medicine-search"
    
    test_queries = [
        "headache",
        "pain",
        "fever",
        "cough",
        "anxiety",
        "turmeric",
        "ibuprofen"
    ]
    
    print("🧪 Testing AI Medicine Search Endpoint")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        
        try:
            response = requests.post(
                url,
                json={"query": query, "limit": 3},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Found {data.get('total_results', 0)} results")
                
                # Show first result if available
                medicines = data.get('medicines', [])
                if medicines:
                    med = medicines[0]
                    print(f"   📋 Top result: {med.get('name', 'Unknown')}")
                    print(f"   🏷️  Category: {med.get('category', 'Unknown')}")
                    print(f"   📊 Confidence: {med.get('confidence_score', 'N/A')}")
                
                # Show AI analysis
                ai_analysis = data.get('ai_analysis', {})
                if ai_analysis:
                    print(f"   🤖 AI Confidence: {ai_analysis.get('confidence', 'N/A')}%")
                    print(f"   📈 Severity: {ai_analysis.get('severity', 'Unknown')}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Medicine search test completed!")

if __name__ == "__main__":
    test_medicine_search()
