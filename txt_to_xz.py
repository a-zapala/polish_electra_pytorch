import argparse
import pathlib
import tarfile
import tempfile
import os
import shutil


class EmptyFile(Exception):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_directory', type=str)
    parser.add_argument('output_directory',type=str)
    parser.add_argument('--lines-per-file', type=int, default=10)
    parser.add_argument('--files-per-tar', type=int, default=10)

                   
    args = parser.parse_args()
    input_dir = pathlib.Path(args.input_directory)
    output_dir = pathlib.Path(args.output_directory)


    if output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir()
    current_tar_index_file = -1

    for file in input_dir.glob("**/*.txt"):
        try:
            with open(file, "r") as f:
                while True:
                    current_tar_index_file+=1
                    with tarfile.open(output_dir / f"{current_tar_index_file}.xz", 'w:xz') as t:
                        for _ in range(args.files_per_tar):
                            content = [next(f) for _ in range(args.lines_per_file)] # discard last lines of file
                            with tempfile.NamedTemporaryFile('w') as tmp:
                                tmp.writelines(content)
                                tmp.seek(0)
                                t.add(tmp.name, arcname=os.path.basename(tmp.name))
                
        except StopIteration:
            pass