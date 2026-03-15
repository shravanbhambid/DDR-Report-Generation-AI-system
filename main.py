import argparse
import os
from pdf_parser import extract_text_from_file
from llm_client import DDRGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate a Detailed Diagnostic Report (DDR) from Site Inspection and Thermal Imaging reports.")
    parser.add_argument("--inspection", "-i", required=True, help="Path to the Site Inspection Report (PDF or TXT)")
    parser.add_argument("--thermal", "-t", required=True, help="Path to the Thermal Imaging Report (PDF or TXT)")
    parser.add_argument("--output", "-o", default="output/DDR_Report.md", help="Path to save the generated markdown report")
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.inspection):
        print(f"Error: Inspection report not found at {args.inspection}")
        return
        
    if not os.path.exists(args.thermal):
        print(f"Error: Thermal report not found at {args.thermal}")
        return
        
    print(f"Loading Site Inspection Report: {args.inspection}")
    inspection_text = extract_text_from_file(args.inspection)
    
    print(f"Loading Thermal Imaging Report: {args.thermal}")
    thermal_text = extract_text_from_file(args.thermal)
    
    # Initialize the generator
    generator = DDRGenerator()
    
    print("Generating DDR report... This uses AI and might take a minute.")
    final_report = generator.generate_report(inspection_text, thermal_text)
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    # Write output file
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(final_report)
        print(f"\nSuccess! Report generated and saved to {args.output}")
    except Exception as e:
        print(f"Error saving report to {args.output}: {e}")

if __name__ == "__main__":
    main()
