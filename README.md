# License Plate Detector

This repository contains a Python application that uses YOLO to detect license plates and exports the model to various formats including ONNX and TensorFlow.js.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository or download the source code.

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To run the application, simply execute the app.py script:

```bash
python app.py
```

This will:
1. Load the YOLO model (`your-model.pt`)
2. Export the model to ONNX format
3. Attempt to export to TensorFlow SavedModel format
4. Convert the model to TensorFlow.js format

## Output Files

After running the application, you should expect the following output files:
- `your-model.onnx`: The ONNX version of the model
- `your-model_saved_model/`: Directory containing the TensorFlow SavedModel
- `tfjs_model/`: Directory containing the TensorFlow.js model

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are correctly installed
2. Check that the model file `your-model.pt` exists in the project directory
3. Ensure you have sufficient disk space for the exported models

## License

This project is licensed under the ISC License.
