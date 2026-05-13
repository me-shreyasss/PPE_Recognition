# PPE Recognition System

## Overview

PPE Recognition System is an AI-powered application that detects and recognizes Personal Protective Equipment (PPE) in images using machine learning. Built with Flask backend and an interactive web interface, this system helps identify whether workers are properly equipped with required safety gear.

## Features

- **AI-Powered Detection**: Uses Roboflow's pre-trained model for accurate PPE detection
- **Real-time Video Streaming**: Live webcam feed with instant PPE detection
- **Color-Coded Annotations**: Green bounding boxes for detected PPE, red for violations
- **Image Upload**: Upload and analyze individual images for detailed predictions
- **Real-time Predictions**: Instant prediction results with confidence scores and labels
- **CORS Enabled**: Cross-origin requests supported for seamless frontend integration
- **Multi-threaded Architecture**: Handles concurrent operations efficiently
- **Modern Web Interface**: Dark theme UI with responsive design
- **Facility Certification**: Helps verify compliance and workplace safety standards
- **Base64 Image Responses**: Prediction results returned as encoded images for easy display

## Project Structure

```
ppe_rec/
├── predictor.py          # Flask backend application
├── index.html            # Main landing page
├── certified.html        # Certification page
├── web2.html            # Web interface template
├── style.css            # Main stylesheet
├── certified.css        # Certification page styles
├── project.js           # Frontend JavaScript
└── templates/           # Flask templates directory
    └── web2.html
```

## Requirements

- Python 3.7+
- Flask
- Flask-CORS
- Roboflow Python SDK
- OpenCV (cv2)
- Modern web browser with webcam support

## Installation

1. **Clone or download the project**
   ```bash
   cd ppe_rec
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask flask-cors roboflow opencv-python
   ```

3. **Ensure webcam access**
   - Grant webcam permissions when prompted by the browser
   - For video streaming, ensure your system has an accessible webcam or camera device

## Usage

1. **Start the Flask application**
   ```bash
   python predictor.py
   ```

2. **Access the web interface**
   - Open your browser and navigate to `http://localhost:5000`
   - Allow webcam permissions when prompted

3. **Video Streaming Mode (Real-time Detection)**
   - Click "Start Stream" to begin live PPE detection from your webcam
   - Watch real-time bounding boxes appear:
     - **Green boxes**: PPE items detected (vest, helmet, mask, etc.)
     - **Red boxes**: Non-PPE or violations detected
   - Click "Stop Stream" to end the live feed

4. **Image Upload Mode**
   - Click on the upload button
   - Select an image containing workers/people with or without PPE
   - The system will analyze the image and return predictions
   - View results with prediction overlays

5. **View Results**
   - For uploaded images: Prediction results displayed with confidence scores
   - For video stream: Real-time annotations on live video feed
   - All predictions follow the same confidence threshold (50% by default)

## API Endpoints

- **GET `/`**: Returns the main web interface (web2.html)
- **GET `/video-stream`**: Streams real-time video frames with PPE detection overlays (MJPEG format)
- **POST `/start-stream`**: Starts the video streaming from webcam
  ```json
  Response: { "status": "streaming started" }
  ```
- **POST `/stop-stream`**: Stops the video streaming
  ```json
  Response: { "status": "streaming stopped" }
  ```
- **POST `/run-script`**: Accepts image file upload and returns prediction results
  ```json
  Response: {
    "result": "Python script has been executed!",
    "prediction_image": "data:image/jpeg;base64,..."
  }
  ```

## Configuration

### Roboflow Model Settings

Edit the following in `predictor.py` to customize:

```python
model.predict(file_path, confidence=50, overlap=30)
```

- **confidence**: Minimum confidence score (0-100) - Predictions below this are filtered
- **overlap**: Non-maximum suppression overlap threshold (0-100) - Controls bounding box filtering

### Upload Folder

The application automatically creates an `uploads/` directory in the project root for storing:
- User-uploaded images
- Temporary frames from video stream
- Prediction results

### CORS Configuration

CORS is enabled by default to allow cross-origin requests. To restrict this, modify:

```python
CORS(app)  # Remove or configure with specific origins
```

### Multi-threading

The Flask app runs with `threaded=True` to handle concurrent video streaming and requests simultaneously.

## Features Implemented

- [x] Image upload and prediction
- [x] Real-time video streaming with detection
- [x] Color-coded bounding boxes (green/red)
- [x] CORS support for cross-origin requests
- [x] Multi-threaded architecture
- [x] Base64 encoded image responses
- [x] Thread-safe streaming controls

## Features to Implement

- [ ] Detailed prediction metrics (detection accuracy, missing PPE items)
- [ ] Batch image processing
- [ ] Database integration for prediction history
- [ ] User authentication and profile management
- [ ] PDF report generation for facility audits
- [ ] Notification system for PPE violations
- [ ] Advanced analytics dashboard

## Security Notes

⚠️ **Important**: 
- Do not commit API keys to version control
- Move API keys to environment variables or a configuration file
- Implement file validation and size limits for uploads
- Validate and sanitize all user inputs
- Restrict webcam access to authorized users in production
- Use HTTPS in production environments
- Consider implementing rate limiting for API endpoints

## UI Features

- **Dark Theme**: Modern dark mode interface with cyan, red, and green accent colors
- **Responsive Design**: Optimized for desktop and tablet views
- **Real-time Updates**: Live video stream with instant visual feedback
- **Intuitive Controls**: Simple start/stop buttons for video streaming
- **Professional Typography**: Space Mono for monospace and DM Sans for body text

## License

[Add your license information here]

## Support

For issues or questions, please contact [your contact information].

## Future Enhancements

- Multi-camera support for monitoring multiple workstations
- Recording capabilities for compliance audits
- PPE compliance scoring system
- Integration with workplace management systems
- Mobile application for on-site inspections
- Enhanced reporting and analytics dashboard
- Machine learning model fine-tuning for custom PPE items
- Alert system for real-time violations
- Export detection history to CSV/PDF
