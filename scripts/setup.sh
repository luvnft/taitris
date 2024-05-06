#!/bin/bash

echo "Installing dependencies..."
npm install

echo "Copying .env.example to .env..."
cp .env.example .env

echo "Setup completed successfully!"