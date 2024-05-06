#!/bin/bash

echo "Building React frontend..."
cd app/frontend
npm run build
cd ../..

echo "Deploying backend..."
cd app/backend
npm run deploy
cd ../..

echo "Applications deployed successfully!"
