// neXtaste Frontend JavaScript with Superhero Effects

// API Configuration
const API_CONFIG = {
    baseUrl: 'http://localhost:8000',
    timeout: 30000,
    retryAttempts: 3
};

// Superhero Brand Manager
class SuperheroBrand {
    constructor() {
        this.loadingDuration = 4000; // 4 seconds for full superhero entrance
        this.xGlowInterval = null;
        this.flickerInterval = null;
    }

    init() {
        this.setupLoadingSequence();
        this.setupBrandInteractions();
        this.setupSuperheroEffects();
    }

    setupLoadingSequence() {
        // Extend loading time for full superhero effect
        setTimeout(() => {
            this.morphLoaderToX();
        }, 1000);

        setTimeout(() => {
            this.triggerBrandEntry();
        }, 2000);

        setTimeout(() => {
            this.activateSlogan();
        }, 2500);

        setTimeout(() => {
            this.completeTransformation();
        }, this.loadingDuration);
    }

    morphLoaderToX() {
        const loader = document.querySelector('.loading-morph');
        if (loader) {
            loader.style.transform = 'scale(1.5) rotateZ(45deg)';
            loader.style.borderRadius = '20%';
            
            // Add X shape morphing
            setTimeout(() => {
                loader.innerHTML = '<span class="text-4xl font-hero text-white animate-x-glow">X</span>';
                loader.style.border = 'none';
                loader.style.background = 'transparent';
            }, 500);
        }
    }

    triggerBrandEntry() {
        const brandLogo = document.querySelector('.brand-logo');
        if (brandLogo) {
            brandLogo.style.opacity = '1';
            brandLogo.style.animation = 'logo-morph 2.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards';
        }

        const brandX = document.querySelector('.brand-x');
        if (brandX) {
            setTimeout(() => {
                brandX.style.animation = 'superhero-entry 2s cubic-bezier(0.68, -0.55, 0.265, 1.55), x-glow 1.5s ease-in-out infinite alternate 2s, x-flicker 0.1s ease-in-out infinite 2s';
            }, 300);
        }
    }

    activateSlogan() {
        const slogan = document.querySelector('.brand-slogan');
        if (slogan) {
            slogan.style.opacity = '1';
            slogan.style.animation = 'slogan-slide 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards';
        }
    }

    completeTransformation() {
        // Trigger the final brand completion effect
        const brandElements = document.querySelectorAll('.brand-transition');
        brandElements.forEach(element => {
            element.style.animation = 'brand-complete 1s ease-out forwards';
        });

        // Activate navigation X glow
        this.activateNavBranding();
    }

    activateNavBranding() {
        const navX = document.querySelector('nav .animate-x-glow');
        if (navX) {
            setInterval(() => {
                navX.style.textShadow = `
                    0 0 ${Math.random() * 20 + 10}px #00d4ff,
                    0 0 ${Math.random() * 30 + 20}px #ff00ff,
                    0 0 ${Math.random() * 40 + 30}px #ffff00
                `;
            }, 100);
        }
    }

    setupBrandInteractions() {
        // Add hover effects to main brand
        document.addEventListener('DOMContentLoaded', () => {
            const brandLogos = document.querySelectorAll('.brand-logo, nav h1');
            
            brandLogos.forEach(logo => {
                logo.addEventListener('mouseenter', () => {
                    const x = logo.querySelector('.brand-x, .animate-x-glow');
                    if (x) {
                        x.style.animation = 'x-glow 0.3s ease-in-out infinite alternate, x-flicker 0.05s ease-in-out infinite';
                        x.style.transform = 'scale(1.2) rotateZ(5deg)';
                    }
                });

                logo.addEventListener('mouseleave', () => {
                    const x = logo.querySelector('.brand-x, .animate-x-glow');
                    if (x) {
                        x.style.animation = 'x-glow 1.5s ease-in-out infinite alternate';
                        x.style.transform = 'scale(1) rotateZ(0deg)';
                    }
                });
            });
        });
    }

    setupSuperheroEffects() {
        // Add random X flicker effects throughout the session
        setInterval(() => {
            const xElements = document.querySelectorAll('.brand-x, .animate-x-glow');
            xElements.forEach(x => {
                if (Math.random() > 0.7) { // 30% chance
                    x.style.animation += ', x-flicker 0.1s ease-in-out 3';
                }
            });
        }, 5000);

        // Add superhero glow to buttons and interactive elements
        this.enhanceInteractiveElements();
    }

    enhanceInteractiveElements() {
        // Add superhero glow to buttons
        const buttons = document.querySelectorAll('button, .btn-primary');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                button.style.boxShadow = '0 0 30px rgba(0, 212, 255, 0.6), 0 0 60px rgba(255, 0, 255, 0.4)';
                button.style.transform = 'translateY(-3px) scale(1.05)';
            });

            button.addEventListener('mouseleave', () => {
                button.style.boxShadow = '';
                button.style.transform = '';
            });
        });
    }

    // Create dynamic background particles
    createSuperheroParticles() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'fixed inset-0 pointer-events-none z-0';
        particleContainer.innerHTML = `
            <div class="absolute inset-0 overflow-hidden">
                ${Array.from({length: 20}, (_, i) => `
                    <div class="absolute w-2 h-2 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full opacity-20"
                         style="
                             left: ${Math.random() * 100}%;
                             top: ${Math.random() * 100}%;
                             animation: float ${3 + Math.random() * 4}s ease-in-out infinite ${Math.random() * 2}s;
                             transform: scale(${0.5 + Math.random()});
                         "></div>
                `).join('')}
            </div>
        `;
        document.body.appendChild(particleContainer);
    }
}

// Initialize superhero brand
const superheroBrand = new SuperheroBrand();

// Utility Functions (Enhanced)
class TasteTrailUtils {
    static formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    static formatRating(rating) {
        return '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    static validateImageUrl(url) {
        const imageExtensions = /\.(jpg|jpeg|png|gif|webp|bmp|svg)$/i;
        return imageExtensions.test(url) || url.includes('unsplash.com') || url.includes('pixabay.com');
    }

    static generateUserId() {
        return 'user_' + Math.random().toString(36).substr(2, 9);
    }

    static getStorageKey(userId, type) {
        return `nextaste_${userId}_${type}`;
    }

    static saveToLocalStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('Failed to save to localStorage:', error);
            return false;
        }
    }

    static loadFromLocalStorage(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('Failed to load from localStorage:', error);
            return null;
        }
    }

    static clearUserData(userId) {
        const keys = ['preferences', 'recommendations', 'analysis_history'];
        keys.forEach(type => {
            const key = this.getStorageKey(userId, type);
            localStorage.removeItem(key);
        });
    }

    // Add superhero toast notifications
    static showSuperheroToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `fixed top-4 right-4 p-4 rounded-lg text-white font-bold z-50 transform transition-all duration-500 ${
            type === 'success' ? 'bg-gradient-to-r from-green-400 to-blue-500' :
            type === 'error' ? 'bg-gradient-to-r from-red-400 to-pink-500' :
            'bg-gradient-to-r from-cyan-400 to-purple-500'
        }`;
        toast.style.boxShadow = '0 0 30px rgba(0, 212, 255, 0.6)';
        toast.innerHTML = `
            <div class="flex items-center space-x-2">
                <span class="animate-x-glow">X</span>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }
}

// Enhanced API Client
class TasteTrailAPI {
    constructor(baseUrl = API_CONFIG.baseUrl) {
        this.baseUrl = baseUrl;
        this.timeout = API_CONFIG.timeout;
        this.retryAttempts = API_CONFIG.retryAttempts;
    }

    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            timeout: this.timeout,
            ...options
        };

        let lastError;
        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.timeout);

                const response = await fetch(url, {
                    ...config,
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
                }

                return await response.json();
            } catch (error) {
                lastError = error;
                if (attempt < this.retryAttempts && !error.name === 'AbortError') {
                    console.warn(`Request attempt ${attempt} failed, retrying...`, error.message);
                    await this.delay(1000 * attempt); // Exponential backoff
                } else {
                    break;
                }
            }
        }

        throw lastError;
    }

    async delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // API Methods
    async checkHealth() {
        return this.makeRequest('/health');
    }

    async getRecommendations(payload) {
        return this.makeRequest('/recommendations-enhanced', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    }

    async getSimilarRestaurants(restaurantName, location = 'New York') {
        return this.makeRequest(`/restaurants/similar/${encodeURIComponent(restaurantName)}?location=${encodeURIComponent(location)}`);
    }

    async analyzeImage(payload) {
        return this.makeRequest('/analyze-food-image', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    }

    async savePreferences(payload) {
        return this.makeRequest('/user-preferences', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    }

    async loadPreferences(userId) {
        return this.makeRequest(`/user-preferences/${userId}`);
    }
}

// Image Analysis Helper
class ImageAnalyzer {
    static async validateImageUrl(url) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => resolve(true);
            img.onerror = () => resolve(false);
            img.src = url;
            
            // Timeout after 5 seconds
            setTimeout(() => resolve(false), 5000);
        });
    }

    static getImageDimensions(url) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                resolve({
                    width: img.naturalWidth,
                    height: img.naturalHeight,
                    aspectRatio: img.naturalWidth / img.naturalHeight
                });
            };
            img.onerror = reject;
            img.src = url;
        });
    }

    static generateThumbnail(file, maxWidth = 300, maxHeight = 300) {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();

            img.onload = () => {
                const { width, height } = this.calculateDimensions(
                    img.width, img.height, maxWidth, maxHeight
                );
                
                canvas.width = width;
                canvas.height = height;
                
                ctx.drawImage(img, 0, 0, width, height);
                resolve(canvas.toDataURL('image/jpeg', 0.8));
            };

            img.src = URL.createObjectURL(file);
        });
    }

    static calculateDimensions(width, height, maxWidth, maxHeight) {
        const ratio = Math.min(maxWidth / width, maxHeight / height);
        return {
            width: width * ratio,
            height: height * ratio
        };
    }
}

// Notification System
class NotificationManager {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.createContainer();
    }

    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.className = 'fixed top-4 right-4 z-50 space-y-2';
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 5000) {
        const notification = this.createNotification(message, type);
        this.container.appendChild(notification);
        
        // Auto remove
        setTimeout(() => {
            this.remove(notification);
        }, duration);

        return notification;
    }

    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `
            notification toast ${type}
            max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto
            flex ring-1 ring-black ring-opacity-5
        `;

        const iconMap = {
            success: 'fas fa-check-circle text-green-500',
            error: 'fas fa-exclamation-circle text-red-500',
            warning: 'fas fa-exclamation-triangle text-yellow-500',
            info: 'fas fa-info-circle text-blue-500'
        };

        notification.innerHTML = `
            <div class="flex-1 w-0 p-4">
                <div class="flex items-start">
                    <div class="flex-shrink-0">
                        <i class="${iconMap[type]} text-xl"></i>
                    </div>
                    <div class="ml-3 w-0 flex-1 pt-0.5">
                        <p class="text-sm font-medium text-gray-900">${message}</p>
                    </div>
                </div>
            </div>
            <div class="flex border-l border-gray-200">
                <button onclick="this.parentElement.parentElement.remove()"
                        class="w-full border border-transparent rounded-none rounded-r-lg p-4
                               flex items-center justify-center text-sm font-medium text-gray-600
                               hover:text-gray-500 focus:outline-none">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        return notification;
    }

    remove(notification) {
        if (notification && notification.parentNode) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }

    success(message, duration) {
        return this.show(message, 'success', duration);
    }

    error(message, duration) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

// Sample Data Generator
class SampleDataGenerator {
    static generateSampleRecommendations() {
        return [
            {
                id: 1,
                name: "Margherita Pizza",
                description: "Classic Italian pizza with fresh mozzarella, tomatoes, and basil",
                cuisine_type: "Italian",
                price: 18.99,
                rating: 4.5,
                image_url: "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=400"
            },
            {
                id: 2,
                name: "Pad Thai",
                description: "Traditional Thai stir-fried noodles with shrimp, tofu, and peanuts",
                cuisine_type: "Thai",
                price: 15.50,
                rating: 4.2,
                image_url: "https://images.unsplash.com/photo-1559314809-0f31657def56?w=400"
            },
            {
                id: 3,
                name: "Chicken Tikka Masala",
                description: "Tender chicken in creamy tomato-based curry sauce",
                cuisine_type: "Indian",
                price: 16.75,
                rating: 4.7,
                image_url: "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400"
            }
        ];
    }

    static generateSampleAnalysis() {
        return {
            detected_foods: [
                {
                    name: "Caesar Salad",
                    confidence: 0.92,
                    nutritional_info: {
                        calories: "320",
                        protein: "15g",
                        carbs: "12g",
                        fat: "25g"
                    }
                }
            ],
            qloo_insights: [
                "Popular among health-conscious diners",
                "Great for lunch or light dinner",
                "Pairs well with white wine"
            ]
        };
    }
}

// Initialize global instances
const tasteTrailAPI = new TasteTrailAPI();
const notificationManager = new NotificationManager();

// Enhanced healthy food carousel with real API integration
function healthyCarousel() {
    return {
        currentSlide: 0,
        foods: [],
        mealType: 'breakfast',
        currentTime: new Date(),
        isLoading: true,
        autoAdvanceInterval: null,
        touchStartX: null,
        
        async init() {
            console.log('🥗 Initializing neXtaste Healthy Carousel...');
            await this.loadHealthyFoods();
            this.startAutoAdvance();
            this.setupKeyboardControls();
        },
        
        async loadHealthyFoods() {
            try {
                this.isLoading = true;
                
                // Get timezone offset
                const timezoneOffset = -new Date().getTimezoneOffset() / 60;
                
                // Call our real API endpoint
                const response = await fetch(`http://localhost:8000/healthy-foods/carousel?timezone_offset=${timezoneOffset}`);
                
                if (response.ok) {
                    const data = await response.json();
                    this.foods = data.foods || [];
                    this.mealType = data.meal_type || 'breakfast';
                    console.log(`🍽️ Loaded ${this.foods.length} ${this.mealType} recommendations from API`);
                } else {
                    throw new Error('API call failed, using fallback data');
                }
            } catch (error) {
                console.warn('⚠️ Using fallback healthy foods data:', error);
                this.loadFallbackFoods();
            } finally {
                this.isLoading = false;
            }
        },
        
        loadFallbackFoods() {
            // Fallback data if API is unavailable
            const hour = new Date().getHours();
            if (hour >= 5 && hour < 11) {
                this.mealType = 'breakfast';
                this.foods = [
                    {
                        name: "Superhero Overnight Oats", 
                        description: "Power-packed oats with chia seeds and berries",
                        calories: 320, protein: 14, carbs: 42, fat: 9,
                        benefits: ["Sustained Energy", "Omega-3", "High Fiber"],
                        image: "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=300&fit=crop"
                    },
                    {
                        name: "X-treme Avocado Toast",
                        description: "Ezekiel bread with smashed avocado and hemp seeds", 
                        calories: 285, protein: 12, carbs: 24, fat: 18,
                        benefits: ["Healthy Fats", "Complete Protein", "B Vitamins"],
                        image: "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400&h=300&fit=crop"
                    }
                ];
            } else if (hour >= 11 && hour < 16) {
                this.mealType = 'lunch';
                this.foods = [
                    {
                        name: "Ultimate Buddha Bowl",
                        description: "Rainbow quinoa bowl with roasted chickpeas",
                        calories: 420, protein: 18, carbs: 52, fat: 16,
                        benefits: ["Complete Nutrition", "Plant-Based", "Anti-Inflammatory"],
                        image: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop"
                    },
                    {
                        name: "Superhero Salmon Bowl",
                        description: "Wild-caught salmon with quinoa and kale",
                        calories: 385, protein: 34, carbs: 28, fat: 16,
                        benefits: ["Omega-3", "Brain Food", "Heart Healthy"],
                        image: "https://images.unsplash.com/photo-1551248429-40975aa4de74?w=400&h=300&fit=crop"
                    }
                ];
            } else if (hour >= 16 && hour < 21) {
                this.mealType = 'dinner';
                this.foods = [
                    {
                        name: "Power Herb-Crusted Chicken",
                        description: "Free-range chicken with sweet potato",
                        calories: 450, protein: 38, carbs: 35, fat: 16,
                        benefits: ["Lean Protein", "Vitamin A", "Iron"],
                        image: "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=400&h=300&fit=crop"
                    }
                ];
            } else {
                this.mealType = 'snack';
                this.foods = [
                    {
                        name: "X-Energy Balls",
                        description: "Dates, almonds, and cacao power spheres",
                        calories: 180, protein: 6, carbs: 22, fat: 8,
                        benefits: ["Natural Energy", "No Added Sugar", "Antioxidants"],
                        image: "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400&h=300&fit=crop"
                    }
                ];
            }
        },
        
        nextSlide() {
            if (this.foods.length === 0) return;
            this.currentSlide = (this.currentSlide + 1) % this.foods.length;
            this.resetAutoAdvance();
        },
        
        prevSlide() {
            if (this.foods.length === 0) return;
            this.currentSlide = this.currentSlide === 0 ? this.foods.length - 1 : this.currentSlide - 1;
            this.resetAutoAdvance();
        },
        
        goToSlide(index) {
            this.currentSlide = index;
            this.resetAutoAdvance();
        },
        
        startAutoAdvance() {
            this.autoAdvanceInterval = setInterval(() => {
                if (this.foods.length > 1) {
                    this.nextSlide();
                }
            }, 5000);
        },
        
        resetAutoAdvance() {
            if (this.autoAdvanceInterval) {
                clearInterval(this.autoAdvanceInterval);
                this.startAutoAdvance();
            }
        },
        
        setupKeyboardControls() {
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    this.prevSlide();
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    this.nextSlide();
                }
            });
        },
        
        // Touch controls
        handleTouchStart(e) {
            this.touchStartX = e.touches[0].clientX;
        },
        
        handleTouchEnd(e) {
            if (!this.touchStartX) return;
            
            const touchEndX = e.changedTouches[0].clientX;
            const diff = this.touchStartX - touchEndX;
            
            if (Math.abs(diff) > 50) { // Minimum swipe distance
                if (diff > 0) {
                    this.nextSlide();
                } else {
                    this.prevSlide();
                }
            }
            
            this.touchStartX = null;
        },
        
        getMealIcon() {
            const icons = {
                breakfast: '🌅',
                lunch: '☀️', 
                dinner: '🌙',
                snack: '⭐'
            };
            return icons[this.mealType] || '🍽️';
        },
        
        getMealGreeting() {
            const greetings = {
                breakfast: 'Power up your morning!',
                lunch: 'Fuel your afternoon!',
                dinner: 'Nourish your evening!',
                snack: 'Smart snacking time!'
            };
            return greetings[this.mealType] || 'Healthy choices await!';
        },
        
        getCurrentFood() {
            return this.foods[this.currentSlide] || {};
        },
        
        destroy() {
            if (this.autoAdvanceInterval) {
                clearInterval(this.autoAdvanceInterval);
            }
        }
    };
}

// Export for use in other scripts
window.TasteTrailUtils = TasteTrailUtils;
window.TasteTrailAPI = TasteTrailAPI;
window.ImageAnalyzer = ImageAnalyzer;
window.NotificationManager = NotificationManager;
window.SampleDataGenerator = SampleDataGenerator;
window.tasteTrailAPI = tasteTrailAPI;
window.notificationManager = notificationManager;
window.healthyCarousel = healthyCarousel;
