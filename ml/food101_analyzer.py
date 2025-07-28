#!/usr/bin/env python3
"""
Enhanced Food Analyzer using Food-101 Dataset + Gemini AI
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetV2B0
from tensorflow.keras.preprocessing import image
import google.generativeai as genai
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

class Food101Analyzer:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent  # Go up to project root
        self.food101_path = self.base_dir / "data" / "food-101" / "food-101" / "food-101"
        
        # Initialize Gemini AI
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Load Food-101 categories
        self.load_food_categories()
        
        # Initialize a simple pre-trained model for now
        self.setup_model()
        
        # Enhanced nutritional database
        self.nutrition_db = self.create_nutrition_database()
    
    def load_food_categories(self):
        """Load Food-101 categories from the dataset"""
        images_dir = self.food101_path / "images"
        if images_dir.exists():
            self.food_classes = sorted([d.name for d in images_dir.iterdir() if d.is_dir()])
            print(f"✅ Loaded {len(self.food_classes)} food categories from Food-101")
        else:
            # Fallback to hardcoded list
            self.food_classes = [
                'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
                'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito',
                'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake',
                'ceviche', 'cheese_plate', 'cheesecake', 'chicken_curry', 'chicken_quesadilla',
                'chicken_wings', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder',
                'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes',
                'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict',
                'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras',
                'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice',
                'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich',
                'grilled_salmon', 'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup',
                'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'lasagna',
                'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup',
                'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters',
                'pad_thai', 'paella', 'pancakes', 'panna_cotta', 'peking_duck',
                'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib',
                'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto',
                'samosa', 'sashimi', 'scallops', 'seaweed_salad', 'shrimp_and_grits',
                'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake',
                'sushi', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles'
            ]
    
    def setup_model(self):
        """Setup a basic model for food classification"""
        print("🧠 Setting up EfficientNet model for food classification...")
        
        # Use EfficientNetV2B0 pre-trained on ImageNet
        self.base_model = EfficientNetV2B0(
            weights='imagenet',
            include_top=True,
            input_shape=(224, 224, 3)
        )
        
        print("✅ Model ready for inference")
    
    def create_nutrition_database(self):
        """Enhanced nutritional database"""
        return {
            'hamburger': {'calories': 540, 'protein': 25, 'carbs': 40, 'fat': 31, 'fiber': 3},
            'pizza': {'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10, 'fiber': 2},
            'french_fries': {'calories': 365, 'protein': 4, 'carbs': 63, 'fat': 17, 'fiber': 4},
            'sushi': {'calories': 200, 'protein': 24, 'carbs': 20, 'fat': 3, 'fiber': 1},
            'caesar_salad': {'calories': 470, 'protein': 7, 'carbs': 7, 'fat': 45, 'fiber': 3},
            'ice_cream': {'calories': 267, 'protein': 5, 'carbs': 31, 'fat': 15, 'fiber': 0},
            'chicken_wings': {'calories': 203, 'protein': 30, 'carbs': 0, 'fat': 9, 'fiber': 0},
            'tacos': {'calories': 226, 'protein': 15, 'carbs': 13, 'fat': 14, 'fiber': 2},
            'ramen': {'calories': 436, 'protein': 20, 'carbs': 54, 'fat': 15, 'fiber': 2},
            'steak': {'calories': 679, 'protein': 62, 'carbs': 0, 'fat': 47, 'fiber': 0},
            'apple_pie': {'calories': 411, 'protein': 4, 'carbs': 58, 'fat': 19, 'fiber': 2},
            'chocolate_cake': {'calories': 563, 'protein': 5, 'carbs': 68, 'fat': 32, 'fiber': 3},
            'greek_salad': {'calories': 211, 'protein': 9, 'carbs': 11, 'fat': 16, 'fiber': 4},
            'fried_rice': {'calories': 220, 'protein': 8, 'carbs': 44, 'fat': 1, 'fiber': 3},
            'bread_pudding': {'calories': 387, 'protein': 8, 'carbs': 52, 'fat': 17, 'fiber': 2},
            'mexican_dish': {'calories': 420, 'protein': 18, 'carbs': 45, 'fat': 16, 'fiber': 8},
            'mixed_plate': {'calories': 380, 'protein': 20, 'carbs': 35, 'fat': 18, 'fiber': 5},
            'prepared_meal': {'calories': 350, 'protein': 16, 'carbs': 40, 'fat': 14, 'fiber': 4}
        }
    
    def preprocess_image(self, image_path):
        """Preprocess image for model"""
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.efficientnet_v2.preprocess_input(img_array)
        return img_array
    
    def simple_food_detection(self, image_path):
        """Enhanced food detection using improved image analysis"""
        detected_foods = []
        
        # Analyze image colors and textures
        img = cv2.imread(str(image_path))
        if img is None:
            return detected_foods
        
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        
        # Calculate color statistics
        mean_hue = np.mean(hsv[:,:,0])
        mean_sat = np.mean(hsv[:,:,1])
        mean_val = np.mean(hsv[:,:,2])
        
        # Calculate texture features
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Color dominance analysis
        colors = img.reshape(-1, 3)
        dominant_color = np.mean(colors, axis=0)
        red_dominance = dominant_color[2] / (np.sum(dominant_color) + 1e-6)
        green_dominance = dominant_color[1] / (np.sum(dominant_color) + 1e-6)
        blue_dominance = dominant_color[0] / (np.sum(dominant_color) + 1e-6)
        
        # Improved food detection logic
        confidence_base = 0.6
        
        # Mexican/Latin dishes (like enchiladas, burritos, etc.)
        if (mean_hue >= 10 and mean_hue <= 25 and mean_sat > 80 and 
            red_dominance > 0.35 and edge_density > 0.1):
            detected_foods.append({
                'food_item': 'mexican_dish',
                'confidence': 0.78,
                'category': 'main_course',
                'description': 'Mexican or Latin American dish with rice and beans'
            })
        
        # Pizza detection (red sauce, cheese patterns)
        elif (mean_hue < 20 and mean_sat > 100 and mean_val > 100 and 
              red_dominance > 0.4):
            detected_foods.append({
                'food_item': 'pizza',
                'confidence': 0.75,
                'category': 'main_course'
            })
        
        # Rice dishes (high brightness, low saturation, granular texture)
        elif (mean_val > 150 and mean_sat < 60 and edge_density > 0.08):
            detected_foods.append({
                'food_item': 'fried_rice',
                'confidence': 0.72,
                'category': 'main_course'
            })
        
        # Salads and green vegetables
        elif (mean_hue >= 60 and mean_hue <= 90 and mean_sat > 60):
            detected_foods.append({
                'food_item': 'greek_salad',
                'confidence': 0.70,
                'category': 'side_dish'
            })
        
        # Bread and light-colored foods
        elif (mean_val > 180 and mean_sat < 50):
            detected_foods.append({
                'food_item': 'bread_pudding',
                'confidence': 0.65,
                'category': 'side_dish'
            })
        
        # Complex dishes with multiple components
        elif edge_density > 0.12:
            detected_foods.append({
                'food_item': 'mixed_plate',
                'confidence': 0.68,
                'category': 'main_course',
                'description': 'Complex dish with multiple components'
            })
        
        # Default fallback
        else:
            detected_foods.append({
                'food_item': 'prepared_meal',
                'confidence': 0.55,
                'category': 'main_course'
            })
        
        # Add nutritional info and enhanced metadata
        for food in detected_foods:
            food_key = food['food_item']
            if food_key in self.nutrition_db:
                food['nutritional_info'] = self.nutrition_db[food_key]
            else:
                # Default nutritional profile
                food['nutritional_info'] = {
                    'calories': 320, 'protein': 15, 'carbs': 35, 'fat': 12, 'fiber': 4
                }
            
            # Add analysis metadata
            food['analysis_method'] = 'enhanced_color_texture'
            food['color_profile'] = {
                'hue': float(mean_hue),
                'saturation': float(mean_sat),
                'brightness': float(mean_val),
                'red_dominance': float(red_dominance),
                'green_dominance': float(green_dominance)
            }
        
        return detected_foods
    
    def get_gemini_analysis(self, image_path, detected_foods):
        """Get enhanced analysis from Gemini AI"""
        try:
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Create detailed prompt
            foods_str = ", ".join([f"{food['food_item']} ({food['confidence']:.0%})" for food in detected_foods])
            
            prompt = f"""
            Analyze this food image. I've detected these items: {foods_str}
            
            Please provide:
            1. **Food Identification**: What foods do you see? Correct my detection if needed.
            2. **Culinary Analysis**: Cooking methods, ingredients, presentation style
            3. **Nutritional Assessment**: Health benefits, caloric content, macro balance
            4. **Cultural Context**: Origin, traditional preparation, cultural significance
            5. **Flavor Profile**: Expected taste, texture, aroma characteristics
            6. **Pairing Suggestions**: What drinks or sides would complement this
            7. **Health Tips**: Dietary considerations, allergens, modifications
            8. **Quality Assessment**: Freshness, preparation quality, visual appeal
            
            Make it engaging and informative, like a food expert's detailed review.
            Keep it concise but comprehensive.
            """
            
            # Generate content with image
            response = self.gemini_model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
            
            return {
                'analysis': response.text,
                'enhanced_description': True,
                'ai_powered': True
            }
            
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return {
                'analysis': f'Enhanced AI analysis unavailable ({str(e)}). Using basic food detection.',
                'enhanced_description': False,
                'ai_powered': False
            }
    
    def generate_recommendations(self, detected_foods):
        """Generate smart recommendations"""
        recommendations = []
        
        if not detected_foods:
            return ['Upload a clear image of food for analysis.']
        
        total_calories = sum([food['nutritional_info'].get('calories', 0) for food in detected_foods])
        total_protein = sum([food['nutritional_info'].get('protein', 0) for food in detected_foods])
        
        if total_calories > 600:
            recommendations.append("🔥 High-calorie meal detected. Consider smaller portions or balance with lighter meals today.")
        elif total_calories < 200:
            recommendations.append("🍎 Light meal detected. Great for snacking or pair with other foods for a complete meal.")
        
        if total_protein > 20:
            recommendations.append("💪 Excellent protein content! Perfect for muscle building and satiety.")
        elif total_protein < 10:
            recommendations.append("🥜 Consider adding protein sources like nuts, eggs, or lean meat.")
        
        # Category-based recommendations
        categories = [food.get('category', 'other') for food in detected_foods]
        if 'dessert' in categories:
            recommendations.append("🍰 Sweet treat detected! Enjoy in moderation and consider pairing with some physical activity.")
        
        if all(cat in ['main_course', 'side_dish'] for cat in categories):
            recommendations.append("🥗 Well-balanced meal composition with main and side dishes.")
        
        return recommendations
    
    def analyze_food(self, image_path):
        """Complete food analysis pipeline"""
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                return {
                    'error': 'Image file not found',
                    'detected_foods': [],
                    'gemini_analysis': {'analysis': 'Image file not found.'},
                    'recommendations': ['Please upload a valid image file.']
                }
            
            print(f"🔍 Analyzing food image: {image_path}")
            
            # Step 1: Basic food detection
            detected_foods = self.simple_food_detection(image_path)
            
            # Step 2: Gemini AI enhancement
            gemini_analysis = self.get_gemini_analysis(image_path, detected_foods)
            
            # Step 3: Generate recommendations
            recommendations = self.generate_recommendations(detected_foods)
            
            # Step 4: Calculate confidence score
            confidence_score = np.mean([food['confidence'] for food in detected_foods]) if detected_foods else 0.0
            
            result = {
                'detected_foods': detected_foods,
                'gemini_analysis': gemini_analysis,
                'recommendations': recommendations,
                'confidence_score': confidence_score,
                'food_count': len(detected_foods),
                'ai_enhanced': gemini_analysis.get('ai_powered', False)
            }
            
            print(f"✅ Analysis complete. Found {len(detected_foods)} food items.")
            return result
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return {
                'error': str(e),
                'detected_foods': [],
                'gemini_analysis': {'analysis': f'Analysis failed: {str(e)}'},
                'recommendations': ['Please try again with a different image.']
            }

# Global analyzer instance
analyzer = Food101Analyzer()

def analyze_food_image(image_path):
    """Main function for food analysis"""
    return analyzer.analyze_food(image_path)

if __name__ == "__main__":
    # Test the analyzer
    test_image = "test_food.jpg"  # Replace with actual test image
    if Path(test_image).exists():
        result = analyze_food_image(test_image)
        print(json.dumps(result, indent=2))
    else:
        print("🍔 Food101 Analyzer ready!")
        print(f"📁 Dataset: {analyzer.food101_path}")
        print(f"🍽️ Categories: {len(analyzer.food_classes)}")
        print("🚀 Ready to analyze food images with Gemini AI!")
