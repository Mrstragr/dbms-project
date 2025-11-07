#!/bin/bash

# SAU Equipment & Lab Resource Management System Setup Script
# This script helps set up the development environment

echo "🚀 Setting up SAU Equipment & Lab Resource Management System..."
echo "================================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Check if MySQL is running
echo "🔍 Checking MySQL connection..."
if command -v mysql &> /dev/null; then
    echo "✅ MySQL client found"
else
    echo "⚠️  MySQL client not found. Please install MySQL or use XAMPP"
fi

# Create necessary directories if they don't exist
echo "📁 Creating project directories..."
mkdir -p templates static/css static/js

echo "✅ Project directories created"

# Set executable permissions
chmod +x app.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Start MySQL server (via XAMPP or local MySQL)"
echo "2. Run the database schema: mysql -u root -p < models.sql"
echo "3. Insert sample data: mysql -u root -p < sample_data.sql"
echo "4. Update database credentials in app.py"
echo "5. Run the application: python3 app.py"
echo ""
echo "🌐 Access the application at: http://localhost:5000"
echo ""
echo "🔐 Default login credentials:"
echo "   Admin: admin@sau.edu / password123"
echo "   Student: john.doe@sau.edu / password123"
echo ""
echo "📚 For more information, see README.md"
echo "================================================================"
