import os
import sys
import argparse
import re

def process_file(filepath, annotation_type):
    """
    Parses a Kubernetes YAML file line-by-line, injecting or updating the
    apphub.cloud.google.com/functional-type annotation for Deployments.
    Handles multiple documents separated by '---'.
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    output_lines = []
    file_modified = False

    def process_document(doc_lines):
        nonlocal file_modified
        out_doc = []
        is_deployment = False

        # Quick pass to see if it's a Deployment
        for line in doc_lines:
            if re.match(r'^kind:\s*Deployment\s*$', line):
                is_deployment = True
                break

        if not is_deployment:
            return doc_lines

        # Full pass to inject annotation
        in_metadata = False
        metadata_indent = -1
        in_annotations = False
        annotations_indent = -1
        annotation_added = False

        for line in doc_lines:
            # Find root metadata block
            metadata_match = re.match(r'^(\s*)metadata:\s*$', line)
            if metadata_match and not in_metadata:
                in_metadata = True
                metadata_indent = len(metadata_match.group(1))
                out_doc.append(line)
                continue

            if in_metadata:
                # Check if we exited metadata block
                current_indent_match = re.match(r'^(\s*)\S', line)
                if current_indent_match:
                    current_indent = len(current_indent_match.group(1))

                    # If we hit a root level key (like spec:) or another block at same level as metadata
                    if current_indent <= metadata_indent and not line.strip().startswith('-'):
                        # If we never found annotations, we need to add the block before we exit metadata
                        if not in_annotations and not annotation_added:
                            new_indent_str = " " * (metadata_indent + 2)
                            out_doc.append(f"{new_indent_str}annotations:\n")
                            out_doc.append(f"{new_indent_str}  apphub.cloud.google.com/functional-type: \"{annotation_type}\"\n")
                            print(f"  Added annotations block and {annotation_type} to {filepath}")
                            file_modified = True
                            annotation_added = True

                        in_metadata = False
                        in_annotations = False
                        out_doc.append(line)
                        continue

                # We are inside metadata. Look for annotations block.
                annotations_match = re.match(r'^(\s*)annotations:\s*$', line)
                if annotations_match and not in_annotations:
                    in_annotations = True
                    annotations_indent = len(annotations_match.group(1))
                    out_doc.append(line)
                    continue

                if in_annotations and not annotation_added:
                    if current_indent_match:
                        current_indent = len(current_indent_match.group(1))
                        # Check if we exited annotations block
                        if current_indent <= annotations_indent and not line.strip().startswith('-'):
                            # Exiting annotations block without finding our target annotation. Add it.
                            new_indent_str = " " * (annotations_indent + 2)
                            out_doc.append(f"{new_indent_str}apphub.cloud.google.com/functional-type: \"{annotation_type}\"\n")
                            print(f"  Added {annotation_type} to existing annotations in {filepath}")
                            file_modified = True
                            annotation_added = True
                            in_annotations = False
                            out_doc.append(line)
                            continue

                    # Look for our specific annotation
                    type_match = re.match(r'^(\s*)apphub\.cloud\.google\.com/functional-type:\s*(.*)$', line)
                    if type_match:
                        existing_val = type_match.group(2).strip()
                        expected_val = f'"{annotation_type}"'
                        if existing_val != expected_val and existing_val != annotation_type:
                            out_doc.append(f"{type_match.group(1)}apphub.cloud.google.com/functional-type: \"{annotation_type}\"\n")
                            print(f"  WARNING: Updated existing functional-type from {existing_val} to {annotation_type} in {filepath}")
                            file_modified = True
                        else:
                            out_doc.append(line)
                            print(f"  Annotation {annotation_type} already exists in {filepath}. Skipping.")
                        annotation_added = True
                        continue

            out_doc.append(line)

        # End of document. If we were still in metadata but never added it (e.g., metadata is the last block)
        if is_deployment and in_metadata and not annotation_added:
            if not in_annotations:
                new_indent_str = " " * (metadata_indent + 2)
                out_doc.append(f"{new_indent_str}annotations:\n")
                out_doc.append(f"{new_indent_str}  apphub.cloud.google.com/functional-type: \"{annotation_type}\"\n")
            else:
                new_indent_str = " " * (annotations_indent + 2)
                out_doc.append(f"{new_indent_str}apphub.cloud.google.com/functional-type: \"{annotation_type}\"\n")
            print(f"  Added {annotation_type} to end of metadata/annotations in {filepath}")
            file_modified = True

        return out_doc

    current_doc = []
    for line in lines:
        if line.strip() == '---':
            output_lines.extend(process_document(current_doc))
            output_lines.append(line)
            current_doc = []
        else:
            current_doc.append(line)

    if current_doc:
        output_lines.extend(process_document(current_doc))

    if file_modified:
        try:
            with open(filepath, 'w') as f:
                f.writelines(output_lines)
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Annotate GKE Deployment YAMLs with Agent Registry functional types.")
    parser.add_argument("folder", help="The folder to recursively search for YAML files.")
    parser.add_argument("type", choices=["AGENT", "MCP_SERVER"], help="The functional type to annotate (AGENT or MCP_SERVER).")

    args = parser.parse_args()

    target_folder = args.folder
    annotation_type = args.type

    if not os.path.isdir(target_folder):
        print(f"Error: Directory '{target_folder}' not found.")
        sys.exit(1)

    print(f"Searching for YAML files in '{target_folder}' to annotate as '{annotation_type}'...")
    print("Warning: This will modify files in-place.\n")

    yaml_count = 0
    for root, _, files in os.walk(target_folder):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                yaml_count += 1
                filepath = os.path.join(root, file)
                process_file(filepath, annotation_type)

    if yaml_count == 0:
        print(f"No .yaml or .yml files found in '{target_folder}'.")
    else:
        print("\nDone processing.")

if __name__ == "__main__":
    main()
