import splitfolders

def div_data():
    # Define input dataset path
    input_folder = "raws/images"  # Ensure your images are structured as dataset/cats/ and dataset/noncats/

    # Define output dataset path
    output_folder = "dataset"

    # Split dataset into train (80%), validation (10%), and test (10%)
    splitfolders.ratio(input_folder, output=output_folder, seed=42, ratio=(0.8, 0.1, 0.1))

    print("Dataset successfully split into train, validation, and test sets.")

div_data()