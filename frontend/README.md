# TasteTrailOps Frontend

A modern, responsive web interface for the TasteTrailOps AI-powered food recommendation system.

## Features

### 🎯 Core Functionality
- **Food Recommendations**: Get personalized food suggestions based on location, meal type, and budget
- **Image Analysis**: Upload food images for AI-powered nutritional analysis
- **User Preferences**: Set dietary restrictions, cuisine preferences, and allergies
- **Real-time API Health Monitoring**: Check backend service status

### 🎨 User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI**: Built with Tailwind CSS for a clean, professional appearance
- **Interactive Elements**: Smooth animations and hover effects
- **Real-time Feedback**: Loading states, success/error notifications
- **Accessibility**: Screen reader friendly with proper ARIA labels

### 🔧 Technical Features
- **Alpine.js**: Lightweight reactive framework for dynamic behavior
- **Tailwind CSS**: Utility-first CSS framework for rapid styling
- **Font Awesome**: Comprehensive icon library
- **Local Storage**: Persistent user preferences
- **Error Handling**: Comprehensive error management with user-friendly messages
- **API Integration**: Full integration with TasteTrailOps backend services

## Quick Start

### Prerequisites
- Python 3.7+ (for the development server)
- TasteTrailOps backend running on `http://localhost:8000`

### Running the Frontend

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Start the development server:**
   ```bash
   python3 server.py
   ```

3. **Open your browser:**
   ```
   http://localhost:3000
   ```

### Alternative: Static File Serving

You can also serve the frontend using any static file server:

```bash
# Using Python's built-in server
python3 -m http.server 3000

# Using Node.js live-server (if installed)
npx live-server --port=3000

# Using nginx (place files in web root)
sudo cp -r . /var/www/html/tastetrail/
```

## File Structure

```
frontend/
├── index.html          # Main application interface
├── styles.css          # Custom CSS styles and animations
├── app.js             # JavaScript utilities and API client
├── server.py          # Development server script
└── README.md          # This file
```

## Usage Guide

### 1. Setting Up User ID
- Enter a unique user ID in the top input field
- This ID will be used to save your preferences and track recommendations
- Example: `user123`, `john_doe`, `foodie2024`

### 2. Getting Recommendations
- **Location**: Enter your city or area (e.g., "New York, NY")
- **Meal Type**: Choose from breakfast, lunch, dinner, or brunch
- **Budget**: Select your price range preference
- Click "Get Recommendations" to see personalized suggestions

### 3. Analyzing Food Images
- Enter a URL to a food image (JPEG, PNG, etc.)
- The AI will identify the food and provide nutritional information
- Results include detected foods with confidence scores and nutrition facts

### 4. Managing Preferences
- **Dietary Restrictions**: Select any dietary needs (vegetarian, vegan, etc.)
- **Cuisine Preferences**: Choose your favorite cuisine types
- **Allergies**: Mark any food allergies for safety
- Save preferences to personalize future recommendations

## API Integration

The frontend communicates with the TasteTrailOps backend through these endpoints:

- `GET /health` - API health check
- `POST /recommendations` - Get food recommendations
- `POST /analyze-food-image` - Analyze food images
- `POST /user-preferences` - Save user preferences
- `GET /user-preferences/{user_id}` - Load user preferences

## Configuration

### Backend URL
By default, the frontend expects the backend to run on `http://localhost:8000`. To change this:

1. Edit the `apiBaseUrl` in `index.html`:
   ```javascript
   apiBaseUrl: 'http://your-backend-url:port'
   ```

2. Or modify the `API_CONFIG` in `app.js`:
   ```javascript
   const API_CONFIG = {
       baseUrl: 'http://your-backend-url:port',
       // ...
   };
   ```

### Server Port
To run the frontend server on a different port, modify `server.py`:

```python
PORT = 3001  # Change to your desired port
```

## Customization

### Styling
- Modify `styles.css` for custom CSS
- Tailwind classes can be changed directly in `index.html`
- Add new color schemes by updating gradient classes

### Functionality
- Extend API methods in `app.js`
- Add new features by modifying the Alpine.js data and methods
- Customize notification system in the `NotificationManager` class

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure the backend is running on `http://localhost:8000`
   - Check if CORS is enabled on the backend
   - Verify the API health check returns success

2. **Frontend Not Loading**
   - Make sure you're accessing `http://localhost:3000/index.html`
   - Check console for JavaScript errors
   - Ensure all CDN resources are loading (check network tab)

3. **Preferences Not Saving**
   - Verify user ID is entered
   - Check browser local storage permissions
   - Ensure backend `/user-preferences` endpoint is working

4. **Images Not Analyzing**
   - Verify image URL is valid and accessible
   - Check if image format is supported (JPG, PNG, etc.)
   - Ensure backend image analysis service is running

### Debug Mode

To enable debug logging, open browser console and run:
```javascript
localStorage.setItem('debug', 'true');
location.reload();
```

## Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## Performance

The frontend is optimized for performance:
- **Lazy Loading**: Images and components load as needed
- **Debounced API Calls**: Prevents excessive API requests
- **Local Caching**: User preferences stored locally
- **Minified Assets**: CDN resources are optimized

## Security

Security measures implemented:
- **Input Validation**: Client-side validation for all user inputs
- **XSS Protection**: Proper escaping of user-generated content
- **CORS Headers**: Proper cross-origin request handling
- **No Sensitive Data**: No API keys or secrets in frontend code

## Contributing

To contribute to the frontend:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly across browsers
5. Submit a pull request

## License

This frontend is part of the TasteTrailOps project and follows the same license terms.
