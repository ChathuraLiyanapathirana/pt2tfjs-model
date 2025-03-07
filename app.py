from ultralytics import YOLO
import os
import subprocess
import sys
import tensorflow as tf

try:
    # Load your YOLO model
    model = YOLO('your-model.pt')
    print("YOLO model loaded successfully")

    # Export to ONNX format
    print("Exporting to ONNX format...")
    onnx_path = model.export(format='onnx', imgsz=[640, 640])
    print(f"ONNX export complete: {onnx_path}")
    
    # Try to export to TensorFlow SavedModel format directly
    # This might work with the latest ultralytics version
    try:
        print("Attempting to export directly to TensorFlow SavedModel format...")
        tf_path = model.export(format='saved_model', imgsz=[640, 640])
        print(f"TensorFlow SavedModel export complete: {tf_path}")
        tf_model_dir = 'your-model_saved_model'
    except Exception as tf_error:
        print(f"TensorFlow SavedModel export failed: {str(tf_error)}")
        print("Will try to convert from ONNX instead.")
        tf_model_dir = None
    
    # Now try to convert to TensorFlow.js format
    tfjs_output_dir = 'tfjs_model'
    
    # If we have a TensorFlow SavedModel, use that for conversion
    if tf_model_dir and os.path.exists(tf_model_dir):
        print("Converting TensorFlow SavedModel to TensorFlow.js...")
        converter_cmd = [
            os.path.join(os.path.dirname(sys.executable), 'tensorflowjs_converter'),
            '--input_format=tf_saved_model',
            '--output_format=tfjs',
            tf_model_dir,
            tfjs_output_dir
        ]
        
        print(f"Running command: {' '.join(converter_cmd)}")
        result = subprocess.run(converter_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Conversion from TensorFlow SavedModel to TensorFlow.js complete!")
        else:
            print(f"TensorFlow SavedModel to TensorFlow.js conversion failed with error:\n{result.stderr}")
            print("Will try alternative approach.")
    
    # If TensorFlow SavedModel conversion failed or we don't have one, try using the Python API directly
    if not os.path.exists(tfjs_output_dir):
        print("Attempting to use tensorflowjs Python API...")
        try:
            import tensorflowjs as tfjs
            from tensorflowjs.converters import convert_tf_saved_model
            
            # If we have a TensorFlow SavedModel, use it
            if tf_model_dir and os.path.exists(tf_model_dir):
                print("Converting TensorFlow SavedModel using Python API...")
                convert_tf_saved_model(tf_model_dir, tfjs_output_dir)
                print("Conversion using Python API successful!")
            else:
                print("No TensorFlow SavedModel available for conversion.")
                print("Please consider using a different approach or installing additional dependencies.")
        except Exception as api_error:
            print(f"Python API conversion failed: {str(api_error)}")
            print("Please consider using a different model format or installing additional dependencies.")
    
    # Check if conversion was successful
    if os.path.exists(tfjs_output_dir) and os.listdir(tfjs_output_dir):
        print("\nConversion successful! TensorFlow.js model is available in the 'tfjs_model' directory.")
        print("You can now use this model in your web application.")
    else:
        print("\nConversion was not successful. Consider the following alternatives:")
        print("1. Use the ONNX model directly with ONNX Runtime Web")
        print("2. Try a different version of TensorFlow and TensorFlow.js")
        print("3. Use a pre-converted model or a different model format")
    
    print("\nAll processing complete! Check the output directories for the converted model.")
except Exception as e:
    print(f"An error occurred: {str(e)}")