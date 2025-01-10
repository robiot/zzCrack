import unittest
import time
from zipfile import ZipFile
from pyzipper import AESZipFile
import zz

# 10kb_1.zip - pwd
# 10kb_2.zip - pass
# 10kb_3.zip - pwd  - AES encrypted
# 10kb_4.zip - hoyo - AES encrypted

zzCrack = zz.zzCrack()

class TestZzCrack(unittest.TestCase):
    def test_bruteforce_1(self):
        start_time = time.time()
        zip_file = ZipFile("10kb_1.zip", "r")
        ret = zzCrack.bruteforce_crack_sp("10kb_1.zip", ZipFile, False, "0", 4)
        elapsed_time = time.time() - start_time
        self.assertEqual(ret, 'pwd')
        print(f"Cost time: {elapsed_time:.3f} seconds")

    def test_bruteforce_2(self):
        start_time = time.time()
        zip_file = ZipFile("10kb_2.zip", "r")
        ret = zzCrack.bruteforce_crack_sp("10kb_2.zip", ZipFile, False, "0", 4)
        elapsed_time = time.time() - start_time
        self.assertEqual(ret, 'pass')
        print(f"Cost time: {elapsed_time:.3f} seconds")

    def test_bruteforce_2_mp4(self):
        start_time = time.time()
        ret = zzCrack.bruteforce_crack_mp("10kb_2.zip", ZipFile, False, "0", 4)
        elapsed_time = time.time() - start_time
        self.assertEqual(ret, 'pass')
        print(f"Cost time: {elapsed_time:.3f} seconds")

    def test_bruteforce_3(self):
        start_time = time.time()
        ret = zzCrack.bruteforce_crack_sp("10kb_3.zip", AESZipFile, False, "0", 4)
        elapsed_time = time.time() - start_time
        self.assertEqual(ret, 'pwd')
        print(f"Cost time: {elapsed_time:.3f} seconds")

    # Single process mode
    # Est. exec time: 2.5 min
    def test_bruteforce_4(self):
        start_time = time.time()
        zip_file = AESZipFile("10kb_4.zip", "r")
        ret = zzCrack.bruteforce_crack_sp("10kb_4.zip", AESZipFile, False, "0", 4)
        elapsed_time = time.time() - start_time
        self.assertEqual(ret, 'hoyo')
        print(f"Cost time: {elapsed_time:.3f} seconds")

    # Default 4 processes
    # Est. exec time: 40 sec
    def test_bruteforce_4_mp4(self):
        start_time = time.time()
        ret = zzCrack.bruteforce_crack_mp("10kb_4.zip", AESZipFile, False, "0", 4)
        elapsed_time = time.time() - start_time
        self.assertEqual(ret, 'hoyo')
        print(f"Cost time: {elapsed_time:.3f} seconds")

    # 16 processes
    # Est. exec time: 20 sec
    def test_bruteforce_4_mp16(self):
        start_time = time.time()
        ret = zzCrack.bruteforce_crack_mp("10kb_4.zip", AESZipFile, False, "0", 4,16)
        elapsed_time = time.time() - start_time
        self.assertEqual(ret, 'hoyo')
        print(f"Cost time: {elapsed_time:.3f} seconds")