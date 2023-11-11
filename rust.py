import ctypes

rust_lib = ctypes.CDLL('rust_code/release/rust.so')

int_to_bytes = lambda x: (x).to_bytes(4, byteorder="little")

rust_lib.function_with_int(int_to_bytes(int(input('Integer to pass: '))))

rust_lib.function_with_string(input('String to pass: ').encode('utf-8'))
