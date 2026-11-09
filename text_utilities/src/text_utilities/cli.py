import argparse
from pathlib import Path

from logic import analyzer, cleaner, counter, process_file, tokenizer

list_commands : list[str] = ["clean", "tokenize", "count", "analyze"]

#Validate txt file as argument

def validate_txt_file(path_str : str) -> Path:
    path = Path(path_str)
    if path.suffix.lower() != '.txt':
        raise argparse.ArgumentTypeError(f"Invalid file '{path_str}. Must be a .txt file")
    return path
    



#Parse User Input

def arg_parser() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser(prog="text_utilities", description="Clean, Tokenize, Count or Analyze txt data")
    
    #Providing strict list of choices to operate
    parser.add_argument(
        "command",
        choices=list_commands,
        help="The operation to execute"
    )
    
    #Passing a valid file ending in .txt
    parser.add_argument(
        "file",
        type=validate_txt_file,
        help="Path to the target .txt file"
    )
    
    #Optional argument
    parser.add_argument(
        "--top",
        type= int,
        default=5,
        help="Number of top frequent items to display (default: 5)"
    )
    
    return parser.parse_args()


def generate_output_file(input_path: Path, command_name: str) -> str:
    return input_path.with_name(f"{input_path.stem}_{command_name}{input_path.suffix}")

def main():
    
    
    args = arg_parser()
    input_file = args.file
    output_file = generate_output_file(input_file, args.command)
    
    processors = {
        "clean" : cleaner,
        "tokenize": tokenizer,
        "count": counter,
    }
        
    if args.command in processors:
        process_file(input_file, output_file, processors[args.command])
        print(f"Successfully processed! Output saved to : {output_file}")
    elif args.command == "analyze":
        raw_text = input_file.read_text(encoding="utf-8")
        
        #Get pydantic model object back
        analysis_report = analyzer(raw_text)
        
        #Turn analysis report into string
        report_text = analysis_report.format_report()
        
        print(report_text)
        
        output_file.write_text(report_text, encoding="utf-8")
        print(f"\nAnalysis report saved to: {output_file}")
    
    
if __name__ == "__main__":
    main()
        
        
        