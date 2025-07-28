# TasteTrailOps

🍽️ **AI-Powered Food Recommendation System with Real-time Analytics**

A comprehensive microservices platform that combines computer vision, machine learning, and real-time data processing to deliver personalized food recommendations with a modern web interface.

## 🚀 Quick Start

### Complete System Demo
```bash
# Clone and start everything
git clone <repository-url>
cd TasteTrailOps
./demo.sh
```

### Manual Setup
```bash
# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Monitoring: http://localhost:3001 (Grafana)
```

## 🎯 Key Features

### 🌐 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live API health monitoring and notifications
- **User-friendly**: Intuitive interface for all features
- **Accessibility**: Screen reader friendly with proper ARIA support

### 🤖 AI-Powered Recommendations
- **Personalized Suggestions**: Based on location, preferences, and dietary restrictions
- **Computer Vision**: Food image analysis with nutritional information
- **Smart Filtering**: Budget-aware and meal-type specific recommendations
- **Qloo Integration**: Enhanced insights from Qloo's taste intelligence API

### 📊 Real-time Analytics
- **Spark Streaming**: Process user interactions and preferences in real-time
- **Feature Engineering**: Dynamic taste profile updates
- **Monitoring Stack**: Prometheus metrics with Grafana dashboards
- **Performance Tracking**: API response times and system health

### 🏗️ Microservices Architecture
- **Scalable Design**: Independent, containerized services
- **Service Discovery**: Proper networking and communication
- **Health Monitoring**: Comprehensive health checks and monitoring
- **Development Ready**: Easy local development and testing

## 🏛️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │   FastAPI       │    │   OpenVINO      │
│   (Port 3000)   │◄──►│   Backend       │◄──►│   Model Server  │
│                 │    │   (Port 8000)   │    │   (Port 9000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐             │
         │              │     Redis       │             │
         └──────────────►│   Cache Layer   │◄────────────┘
                        │   (Port 6379)   │
                        └─────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │                                                 │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Apache Kafka  │    │   Apache Spark  │    │     Feast       │
│   Event Stream  │◄──►│   Streaming     │◄──►│ Feature Store   │
│   (Port 9092)   │    │   (Port 8080)   │    │   (Port 6566)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
    ┌─────────────────┐    ┌─────────────────┐
    │   Prometheus    │    │     Grafana     │
    │   Metrics       │◄──►│   Dashboards    │
    │   (Port 9090)   │    │   (Port 3001)   │
    └─────────────────┘    └─────────────────┘
```

## 📱 User Interface

### Dashboard Overview
The frontend provides three main sections:

1. **🌟 Recommendations Tab**
   - Location-based food suggestions
   - Meal type and budget filtering
   - Real-time results with ratings and prices

2. **📸 Food Analysis Tab**
   - Upload food images for AI analysis
   - Nutritional information extraction
   - Ingredient identification and confidence scores

3. **⚙️ Preferences Tab**
   - Dietary restrictions management
   - Cuisine preferences selection
   - Allergy tracking and safety features

### API Integration
- **Health Monitoring**: Real-time backend status
- **Error Handling**: User-friendly error messages
- **Loading States**: Clear feedback during operations
- **Local Storage**: Persistent user preferences

## 🔧 Services Overview

| Service | Purpose | Port | Technology |
|---------|---------|------|------------|
| **Frontend** | Web UI | 3000 | HTML/CSS/JS + Tailwind |
| **API** | Backend Logic | 8000 | FastAPI + Python |
| **OpenVINO** | Computer Vision | 9000 | Intel OpenVINO |
| **Redis** | Caching | 6379 | Redis |
| **Kafka** | Event Streaming | 9092 | Apache Kafka |
| **Spark** | Stream Processing | 8080 | Apache Spark |
| **Feast** | Feature Store | 6566 | Feast |
| **Prometheus** | Metrics | 9090 | Prometheus |
| **Grafana** | Dashboards | 3001 | Grafana |