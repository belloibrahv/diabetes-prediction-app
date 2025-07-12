#!/bin/bash

# Diabetes Prediction App - Vercel Deployment Script

echo "🚀 Setting up Vercel deployment for Diabetes Prediction App..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in the correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the flask directory."
    exit 1
fi

# Check if all required files exist
required_files=("app.py" "requirements.txt" "vercel.json" "model.pkl" "scaler.pkl" "label_encoders.pkl" "feature_names.pkl")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Required file $file not found."
        exit 1
    fi
done

echo "✅ All required files found."

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "📝 Your app should now be live on Vercel."
echo "🔗 Check your Vercel dashboard for the deployment URL." 