#!/bin/bash
# GitHub Deployment Script for avinash4u
echo "🚀 Deploying Medical Device Classifier to GitHub..."
echo ""

# Step 1: Set remote URL
git remote set-url origin https://github.com/avinash4u/medical_device_classifier.git
echo "✅ Remote URL set to: https://github.com/avinash4u/medical_device_classifier.git"

# Step 2: Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "🎉 Deployment complete!"
echo "📍 Your repository will be available at: https://github.com/avinash4u/medical_device_classifier"
