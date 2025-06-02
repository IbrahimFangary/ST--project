# pip install GEOparse git+https://github.com/IbrahimFangary/cloupe_image.git


import urllib.request
import os
import gzip
import shutil
import Cloupe_image
import GEOparse
os.makedirs('data')
os.chdir('data')

base_dir = os.getcwd()

gse = GEOparse.get_GEO("GSE210616", destdir="./geo_data")

def unzip_cloupe_file(gz_path):
    if not gz_path.endswith('.gz'):
        print(f"[!] Not a .gz file: {gz_path}")
        return

    output_path = gz_path[:-3]
    if os.path.exists(output_path):
        return

    try:
        with gzip.open(gz_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(gz_path)

    except Exception as e:
        print(f"[!] Failed to unzip {gz_path}: {e}")

for gsm_id in gse.gsms.keys():

    os.chdir(base_dir)
    title = gse.gsms[gsm_id].metadata['title'][0]


    parts = title.split(', ')
    patient_info = parts[1].strip()
    section_info = parts[2].strip()

    # Clean names
    patient_dir = f"{patient_info.replace(' ', '_')}"
    section_dir = f"{section_info.replace(' ', '_')}"

    full_dir_path = os.path.join(patient_dir, section_dir)
    os.makedirs(full_dir_path, exist_ok=True)

    cloupe_url = gse.gsms[gsm_id].metadata['supplementary_file_1'][0]

    if 'cloupe' in cloupe_url:
        filename = cloupe_url.split('/')[-1]
        output_path = os.path.join(full_dir_path, filename)
        print(f"Downloading {filename} to {full_dir_path}")
        try:
            urllib.request.urlretrieve(cloupe_url, output_path)
        except Exception as e:
            print(f"Failed to download {cloupe_url}: {e}")

        unzip_cloupe_file(output_path)

        os.chdir(os.path.join(base_dir, full_dir_path))
        Cloupe_image.stitch_cloupe_image(os.path.join(base_dir, output_path.split('.gz')[0]))

        os.rename('stitched_highres.tiff', f"{filename.split('.cloupe.gz')[0]}_stitched_highres.tiff")
        os.rename('stitched_downsampled.tiff', f"{filename.split('.cloupe.gz')[0]}_stitched_downsampled.tiff")
        os.remove(os.path.join(base_dir, output_path.split('.gz')[0]))
