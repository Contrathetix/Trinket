import os
import sys
import time
import logging
import zipfile
import urllib.request

import shared.modulebase


class TTCData(shared.modulebase.ModuleBase):

    def preferred_load_index(self) -> int:
        return 9

    def update(self) -> None:
        logging.info('update...')
        if self.is_update_needed():
            logging.info('update needed, downloading...')
            self.download()
            logging.info('download finished, unpacking...')
            self.unpack()
            logging.info('update finished')
        else:
            logging.info('update not needed')

    def download(self) -> None:
        zip_path = self.get_temp_zip_path()
        zip_age = self.get_file_age_minutes(zip_path)
        zip_age_max = self.app.config.get('ttc.download.max_age_minutes')
        if (zip_age > 0 and zip_age < zip_age_max):
            logging.info('use cached zip')
            return
        download_url = self.app.config.get('ttc.download.source_url')
        logging.info('fetching data from \'{}\''.format(download_url))
        try:
            response = urllib.request.urlopen(download_url)
            headers = dict(response.getheaders())
            bytes_accumulator = bytearray()
            bytes_total = int(headers.get('Content-Length'))
            bytes_step = int(bytes_total / 50)
            bytes_current = 0
            logging.info('need to fetch {} bytes ({} MB)'.format(
                bytes_total, round(bytes_total/1024000, 3)
            ))
            while (bytes_current < bytes_total):
                # time.sleep(0.1)
                # sys.stdout.write('\rTTC Data: downloading {}/{} ({}%)'.
                # format(
                #    bytes_current, bytes_total,
                #    round(100*(bytes_current / bytes_total), 1)
                # ))
                # sys.stdout.flush()
                bytes_current = min(
                    int(bytes_current + bytes_step), bytes_total
                )
                bytes_accumulator.extend(response.read(bytes_current))
            # sys.stdout.write('\n')
            bytes_accumulated = len(bytes_accumulator)
            logging.info('fetched total {}/{} bytes'.format(
                bytes_accumulated, bytes_total
            ))
            if (bytes_accumulated != bytes_total):
                logging.info('fetched different count of bytes than intended?')
            else:
                ttc_data = bytes_accumulator
        except Exception as exc:
            logging.error(exc)
        if ttc_data:
            logging.info('saving zip to: {}'.format(zip_path))
            with open(zip_path, 'wb') as zip_fp:
                zip_fp.write(ttc_data)

    def get_temp_zip_path(self) -> str:
        return os.path.join(
            self.app.path,
            'data',
            self.app.config.get('ttc.download.zip_file_name')
        )

    def get_file_age_minutes(self, file_path):
        if (not os.path.isfile(file_path)):
            return -1
        else:
            file_mtime = os.stat(file_path).st_mtime
            current_time = time.time()
            file_age_minutes = int((current_time - file_mtime) / 60)
            return file_age_minutes

    def unpack(self) -> None:
        temp_zip = self.get_temp_zip_path()
        extract_target = self.app.config.get('ttc.data.extraction_path')
        logging.info('extracting files from zip...')
        with zipfile.ZipFile(temp_zip, 'r') as zip_fp:
            for filename in zip_fp.namelist():
                if not filename.endswith('.lua'):
                    continue
                target_path = os.path.join(extract_target, filename)
                logging.info('extract: {} -> {}'.format(filename, target_path))
                zip_fp.extract(filename, extract_target)
        logging.info('extraction finished')

    def is_update_needed(self) -> bool:
        test_file = self.app.config.get('ttc.data.age_test_file')
        if not os.path.isfile(test_file):
            logging.info('file does not exist at \'{}\''.format(test_file))
            return True
        max_age_minutes = self.app.config.get('ttc.data.max_age_minutes')
        file_age_minutes = self.get_file_age_minutes(test_file)
        logging.info('file age {} minutes, max {} minutes'.format(
            file_age_minutes, max_age_minutes
        ))
        if (file_age_minutes < 0 or file_age_minutes > max_age_minutes):
            return True
        else:
            return False
