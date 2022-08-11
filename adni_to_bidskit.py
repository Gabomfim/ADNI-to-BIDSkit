import argparse
import pathlib
import shutil

def get_BIDS_name(dirname):
  return dirname.replace('-','').replace('_','').replace('.','')

parser = argparse.ArgumentParser(description='rearranges an ADNI dataset according to BIDS standard.')
parser.add_argument('-d', '--dataset', required=True,
                    help='path to the dataset you wish rearrange accordingly to BIDS standard.')

args = parser.parse_args()

dataset_path = pathlib.Path(args.dataset)
output_path = pathlib.Path('sourcedata')

shutil.rmtree(output_path, ignore_errors=True)

output_path.mkdir(exist_ok=True)

subject_paths = dataset_path.glob('*')
subject_dirs = [subject_dir for subject_dir in subject_paths if subject_dir.is_dir()]

for index, subject_dir in enumerate(subject_dirs):
  new_subject_name = get_BIDS_name(subject_dir.name)

  new_subject_path = output_path.joinpath(new_subject_name)
  new_subject_path.mkdir(parents=True, exist_ok=True)

  session_paths = subject_dir.glob('*/*')
  session_dirs = [session_dir for session_dir in session_paths if session_dir.is_dir()]

  for index, session_dir in enumerate(session_dirs):
    new_session_name = str(index+1).zfill(3)

    new_session_path = new_subject_path.joinpath(new_session_name)
    new_session_path.mkdir(parents=True, exist_ok=True)

    dicom_dir = session_dir.glob('*/*')

    for index, dicom_file_path in enumerate(dicom_dir):
      new_dicom_file_path = new_session_path.joinpath(get_BIDS_name(dicom_file_path.stem)+'.dcm')
      shutil.copy(dicom_file_path, new_dicom_file_path)