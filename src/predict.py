import joblib
import pandas as pd
import numpy as np

MODEL_VERSION = '1.0.0'

def _extract_model(loaded_obj):
    # Support both direct estimators and dict-wrapped saved artifacts
    if hasattr(loaded_obj, 'predict') and hasattr(loaded_obj, 'predict_proba'):
        return loaded_obj
    if isinstance(loaded_obj, dict):
        preferred_keys = ('model', 'estimator', 'classifier', 'best_model', 'pipeline')
        for key in preferred_keys:
            candidate = loaded_obj.get(key)
            if hasattr(candidate, 'predict') and hasattr(candidate, 'predict_proba'):
                return candidate
        for candidate in loaded_obj.values():
            if hasattr(candidate, 'predict') and hasattr(candidate, 'predict_proba'):
                return candidate
    raise TypeError(f"Loaded object is not a valid model type: {type(loaded_obj)}")

# Load the model ONCE at module level
try:
    model = joblib.load('model/heatwave_model.pkl')
    model = _extract_model(model)
    print("[OK] Model loaded successfully")
except FileNotFoundError:
    print("[ERROR] Model file not found at 'model/heatwave_model.pkl'")
    model = None
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")
    model = None

def predict_heatwave(features):
    """
    Predict heatwave probability
    
    Args:
        features: list or array of features [f1, f2, f3, ...]
    
    Returns:
        tuple: (prediction, probability)
    """
    if model is None:
        raise RuntimeError("Model not loaded. Check file path.")
    
    # Reshape to 2D array for sklearn
    input_data = features.values.reshape(1, -1) if hasattr(features, 'values') else np.array(features).reshape(1, -1)
    
    # Get prediction
    prediction = model.predict(input_data)[0]
    
    # Get probability for class 1 (Heatwave)
    probability = model.predict_proba(input_data)[0][1]
    
    return prediction, probability

# Example usage:
if __name__ == "__main__":
    # Test with sample features
    test_features = [25.5, 60, 1013, 5]  # Example: temp, humidity, pressure, wind
    try:
        pred, prob = predict_heatwave(test_features)
        print(f"Prediction: {pred}, Probability: {prob:.2%}")
    except Exception as e:
        print(f"Error during prediction: {e}")