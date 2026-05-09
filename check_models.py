"""
Check available embedding models in Google Generative AI
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("🔍 Checking available embedding models...\n")

try:
    # List all available models
    models = genai.list_models()
    
    print("=" * 80)
    print("ALL AVAILABLE MODELS:")
    print("=" * 80)
    
    embedding_models = []
    text_models = []
    
    for model in models:
        # Print all models for reference
        print(f"\n📌 {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Supported Methods: {model.supported_generation_methods}")
        
        # Categorize by capability
        if "embedContent" in model.supported_generation_methods:
            embedding_models.append(model.name)
            print("   ✅ SUPPORTS EMBEDDING")
        
        if "generateContent" in model.supported_generation_methods:
            text_models.append(model.name)
            print("   ✅ SUPPORTS TEXT GENERATION")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    
    print("\n🔷 EMBEDDING MODELS (embedContent):")
    if embedding_models:
        for model in embedding_models:
            print(f"  ✅ {model}")
    else:
        print("  ❌ No embedding models found")
    
    print("\n📝 TEXT GENERATION MODELS (generateContent):")
    if text_models:
        for model in text_models:
            print(f"  ✅ {model}")
    else:
        print("  ❌ No text generation models found")
    
    # Recommendation
    print("\n" + "=" * 80)
    print("RECOMMENDED MODELS TO USE:")
    print("=" * 80)
    
    if embedding_models:
        print(f"\n📌 For Embeddings: {embedding_models[0]}")
        print(f"   (Use this in get_embeddings() function)")
    
    if text_models:
        print(f"\n📌 For Text Generation: {text_models[0]}")
        print(f"   (Use this in generate_answer() function)")
    
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nNote: Make sure your GEMINI_API_KEY is valid and you have internet connection.")
