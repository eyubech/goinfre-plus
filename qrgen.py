import qrcode

def print_qr_code_in_terminal(url):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # about 7% error correction
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Print the QR code as ASCII in the terminal
    qr.print_ascii(tty=True)  # Use `tty=True` to print using terminal-friendly characters

# Example usage
url = "http://192.168.214.127:4242/"
print_qr_code_in_terminal(url)
