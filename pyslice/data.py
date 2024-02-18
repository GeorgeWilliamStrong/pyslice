import os
import shutil
import urllib.request
from tqdm import tqdm
import zipfile
import nibabel as nib
import numpy as np


__all__ = ['ICBM2009NonLinSym']


class ICBM2009NonLinSym:
    def __init__(self, remove_zip=True):
        """
        Initialize the ICBM2009NonLinSym class. This will automatically
        download the ICBM 2009c Nonlinear Symmetric brain template. More
        information can be found here:
        http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009.

        The data will be loaded and stored in self.dict.

        Parameters
        ----------
        remove_zip : bool, optional
            If True, remove the downloaded zip file after extraction.
            Default is True.
        """
        self.name = 'mni_icbm152_nlin_sym_09c_nifti'
        self.fname = f'{self.name}.zip'
        self.dir_name = 'mni_icbm152_nlin_sym_09c'
        self.url = 'https://www.bic.mni.mcgill.ca/~vfonov/icbm/2009/' + \
            self.fname
        self.download_path = './data'
        self.dir = os.path.join(self.download_path, self.dir_name)
        zip_file_path = os.path.join(self.download_path, f'{self.name}.zip')

        if not os.path.exists(self.dir):
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024,
                      miniters=1, desc='Downloading') as t:
                urllib.request.urlretrieve(self.url,
                                           zip_file_path,
                                           reporthook=lambda count,
                                           block_size,
                                           total_size: _progress(count,
                                                                 block_size,
                                                                 total_size,
                                                                 t))

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.download_path)

            if remove_zip:
                for dir in os.listdir(self.download_path):
                    if dir != self.dir_name:
                        _remove_path(os.path.join(self.download_path, dir))

        b = os.path.join(self.dir, 'mni_icbm152_')
        m = '_tal_nlin_sym_09c'
        e = '.nii'
        self.dict = {
            't1': np.flipud(np.array(nib.load(
                f'{b}t1{m}{e}').get_fdata()).T),
            't2': np.flipud(np.array(nib.load(
                f'{b}t2{m}{e}').get_fdata()).T),
            'brain': np.flipud(np.array(nib.load(
                f'{b}t1{m}_mask{e}').get_fdata()).T),
            'eyes': np.flipud(np.array(nib.load(
                f'{b}t1{m}_eye_mask{e}').get_fdata()).T),
            'face': np.flipud(np.array(nib.load(
                f'{b}t1{m}_face_mask{e}').get_fdata()).T),
            'gm': np.flipud(np.array(nib.load(
                f'{b}gm{m}{e}').get_fdata()).T),
            'wm': np.flipud(np.array(nib.load(
                f'{b}wm{m}{e}').get_fdata()).T),
            'csf': np.flipud(np.array(nib.load(
                f'{b}csf{m}{e}').get_fdata()).T)
        }


def _progress(count, block_size, total_size, t):
    if count == 0:
        t.total = total_size
        t.refresh()
    progress_size = int(count * block_size)
    t.update(progress_size - t.n)


def _remove_path(path):
    try:
        shutil.rmtree(path)
    except OSError:
        try:
            os.remove(path)
        except OSError as e:
            print(f"Error: {e}")
